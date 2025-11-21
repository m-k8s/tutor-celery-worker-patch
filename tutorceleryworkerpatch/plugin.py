"""
Tutor plugin to customize Celery worker parameters for LMS and CMS.

This plugin allows you to configure Celery worker arguments like concurrency,
max-tasks-per-child, prefetch-multiplier, and queues via Tutor configuration.

It uses Tutor's built-in hooks to override the default Celery worker commands.
"""
from __future__ import annotations

import typing as t

from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

# Configuration defaults for the plugin
config: dict[str, dict[str, t.Any]] = {
    "defaults": {
        "VERSION": __version__,
        # CMS Worker settings
        "CMS_CONCURRENCY": 1,
        "CMS_MAX_TASKS_PER_CHILD": 100,
        "CMS_PREFETCH_MULTIPLIER": 1,
        "CMS_QUEUES": "edx.cms.core.default,edx.cms.core.high,edx.cms.core.low",
        # LMS Worker settings
        "LMS_CONCURRENCY": 1,
        "LMS_MAX_TASKS_PER_CHILD": 100,
        "LMS_PREFETCH_MULTIPLIER": 1,
        "LMS_QUEUES": "edx.lms.core.default,edx.lms.core.high,edx.lms.core.high_mem",
    },
}

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"CELERY_WORKER_PATCH_{key}", value) for key, value in config.get("defaults", {}).items()]
)


# Store for configuration values loaded at runtime
_config_store: dict[str, t.Any] = {}


@tutor_hooks.Actions.CONFIG_LOADED.add()
def _on_config_loaded(config: dict[str, t.Any]) -> None:
    """
    Store configuration values when config is loaded.
    """
    _config_store.update(config)


@tutor_hooks.Filters.LMS_WORKER_COMMAND.add()
def _override_lms_worker_command(commands: list[str]) -> list[str]:
    """
    Override the LMS Celery worker command with custom parameters.

    This replaces the default command entirely with our optimized configuration.
    """
    concurrency = _config_store.get("CELERY_WORKER_PATCH_LMS_CONCURRENCY", 1)
    max_tasks = _config_store.get("CELERY_WORKER_PATCH_LMS_MAX_TASKS_PER_CHILD", 100)
    prefetch = _config_store.get("CELERY_WORKER_PATCH_LMS_PREFETCH_MULTIPLIER", 1)
    queues = _config_store.get(
        "CELERY_WORKER_PATCH_LMS_QUEUES",
        "edx.lms.core.default,edx.lms.core.high,edx.lms.core.high_mem"
    )

    return [
        "celery",
        "--app=lms.celery",
        "worker",
        "--loglevel=info",
        f"--concurrency={concurrency}",
        "--hostname=edx.lms.core.default.%h",
        f"--queues={queues}",
        f"--max-tasks-per-child={max_tasks}",
        f"--prefetch-multiplier={prefetch}",
        "--without-gossip",
        "--without-mingle",
    ]


@tutor_hooks.Filters.CMS_WORKER_COMMAND.add()
def _override_cms_worker_command(commands: list[str]) -> list[str]:
    """
    Override the CMS Celery worker command with custom parameters.

    This replaces the default command entirely with our optimized configuration.
    """
    concurrency = _config_store.get("CELERY_WORKER_PATCH_CMS_CONCURRENCY", 1)
    max_tasks = _config_store.get("CELERY_WORKER_PATCH_CMS_MAX_TASKS_PER_CHILD", 100)
    prefetch = _config_store.get("CELERY_WORKER_PATCH_CMS_PREFETCH_MULTIPLIER", 1)
    queues = _config_store.get(
        "CELERY_WORKER_PATCH_CMS_QUEUES",
        "edx.cms.core.default,edx.cms.core.high,edx.cms.core.low"
    )

    return [
        "celery",
        "--app=cms.celery",
        "worker",
        "--loglevel=info",
        f"--concurrency={concurrency}",
        "--hostname=edx.cms.core.default.%h",
        f"--queues={queues}",
        f"--max-tasks-per-child={max_tasks}",
        f"--prefetch-multiplier={prefetch}",
        "--without-gossip",
        "--without-mingle",
    ]
