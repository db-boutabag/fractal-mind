#!/bin/bash
#
# fractal-mind Shared Vault Auto-Sync
#
# Automatically syncs a git-managed shared vault folder. Features:
# - Lock file to prevent concurrent runs
# - Log rotation (max 500 lines)
# - Check for changes → stage → commit → pull (rebase) → push
# - Dry-run mode (--dry-run flag)
# - Optional mirror.conf support for one-way syncs
#
# Configure SHARED_DIR below, then use with launchd for automated sync.
#

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

# EDIT THIS: Path to your Shared/ vault directory
SHARED_DIR="/path/to/your/vault/Shared"

# Log file
LOG_FILE="${SHARED_DIR}/.sync.log"

# Lock file to prevent concurrent runs
LOCK_FILE="${SHARED_DIR}/.sync.lock"

# Maximum log lines before rotation
MAX_LOG_LINES=500

# ============================================================================
# Functions
# ============================================================================

log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $*" >> "${LOG_FILE}"
}

log_and_echo() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $*" | tee -a "${LOG_FILE}"
}

rotate_log() {
    if [ ! -f "${LOG_FILE}" ]; then
        return
    fi

    local line_count
    line_count=$(wc -l < "${LOG_FILE}")

    if [ "${line_count}" -gt "${MAX_LOG_LINES}" ]; then
        tail -n "${MAX_LOG_LINES}" "${LOG_FILE}" > "${LOG_FILE}.tmp"
        mv "${LOG_FILE}.tmp" "${LOG_FILE}"
        log "Log rotated (was ${line_count} lines)"
    fi
}

acquire_lock() {
    local max_wait=30
    local elapsed=0

    while [ -f "${LOCK_FILE}" ] && [ "${elapsed}" -lt "${max_wait}" ]; do
        sleep 1
        elapsed=$((elapsed + 1))
    done

    if [ -f "${LOCK_FILE}" ]; then
        log_and_echo "Error: Could not acquire lock after ${max_wait}s. Aborting."
        exit 1
    fi

    echo "$$" > "${LOCK_FILE}"
}

release_lock() {
    rm -f "${LOCK_FILE}"
}

cleanup() {
    release_lock
}

trap cleanup EXIT

validate_shared_dir() {
    if [ ! -d "${SHARED_DIR}" ]; then
        log_and_echo "Error: SHARED_DIR does not exist: ${SHARED_DIR}"
        exit 1
    fi

    if [ ! -d "${SHARED_DIR}/.git" ]; then
        log_and_echo "Error: SHARED_DIR is not a git repository: ${SHARED_DIR}"
        exit 1
    fi
}

sync_vault() {
    local dry_run="${1:-false}"

    cd "${SHARED_DIR}"

    # Check for changes
    local has_changes
    has_changes=$(git status --porcelain | wc -l)

    if [ "${has_changes}" -eq 0 ]; then
        log "No changes detected"
        return
    fi

    log "Detected ${has_changes} change(s)"

    if [ "${dry_run}" = "true" ]; then
        log "[DRY-RUN] Would stage and commit changes"
        git status --short | while read -r line; do
            log "[DRY-RUN] Change: ${line}"
        done
        return
    fi

    # Stage all changes
    git add -A
    log "Staged changes"

    # Create commit with timestamp
    local commit_msg
    commit_msg="Shared vault sync — $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "${commit_msg}" || log "Commit failed or no staged changes"

    # Pull with rebase to avoid merge commits
    if ! git pull --rebase origin main 2>&1 | while read -r line; do log "Pull: ${line}"; done; then
        log "Error: Pull with rebase failed. Manual intervention needed."
        return 1
    fi

    log "Pull successful (rebased)"

    # Push changes
    if ! git push origin main 2>&1 | while read -r line; do log "Push: ${line}"; done; then
        log "Error: Push failed. Your changes may still be local."
        return 1
    fi

    log "Push successful"
}

mirror_sync() {
    # Optional: implement one-way mirror from personal vault to shared
    # Requires mirror.conf file with source/destination mappings
    #
    # mirror.conf format:
    #   /path/to/personal/file.md -> Shared/Meeting-Notes/file.md
    #
    local mirror_conf="${SHARED_DIR}/mirror.conf"

    if [ ! -f "${mirror_conf}" ]; then
        return
    fi

    local dry_run="${1:-false}"

    log "Processing mirror.conf"

    while IFS=' -> ' read -r src dest; do
        # Skip comments and empty lines
        [[ "${src}" =~ ^# ]] && continue
        [ -z "${src}" ] && continue

        if [ ! -f "${src}" ]; then
            log "Mirror: source file not found: ${src}"
            continue
        fi

        local dest_path="${SHARED_DIR}/${dest}"
        local dest_dir
        dest_dir=$(dirname "${dest_path}")

        if [ "${dry_run}" = "true" ]; then
            log "[DRY-RUN] Would mirror: ${src} -> ${dest}"
            continue
        fi

        mkdir -p "${dest_dir}"
        cp "${src}" "${dest_path}"
        log "Mirrored: ${src} -> ${dest}"
    done < "${mirror_conf}"
}

# ============================================================================
# Main
# ============================================================================

main() {
    local dry_run="false"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run)
                dry_run="true"
                shift
                ;;
            *)
                log_and_echo "Unknown argument: $1"
                exit 1
                ;;
        esac
    done

    validate_shared_dir
    rotate_log

    acquire_lock
    log_and_echo "=== Sync started $([ "${dry_run}" = "true" ] && echo '[DRY-RUN]' || true)"

    if [ "${dry_run}" = "true" ]; then
        log "[DRY-RUN] mode enabled"
    fi

    sync_vault "${dry_run}"
    mirror_sync "${dry_run}"

    log_and_echo "=== Sync complete"
}

main "$@"
