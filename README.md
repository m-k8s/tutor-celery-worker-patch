# Tutor Celery Worker Patch Plugin

A Tutor plugin to customize Celery worker parameters for LMS and CMS workers.

## Features

This plugin allows you to configure the following Celery worker parameters:

- **Concurrency**: Number of worker processes (default: 1)
- **Max tasks per child**: Number of tasks before worker restart (default: 100)
- **Prefetch multiplier**: Number of tasks to prefetch (default: 1)
- **Queues**: Which queues the worker listens to

The plugin also enables these Celery optimizations by default:
- `--without-gossip`: Disable worker coordination
- `--without-mingle`: Disable startup synchronization

## Installation

```bash
pip install -e ./tutor-celery-worker-patch
```

## Enable the plugin

```bash
tutor plugins enable celery-worker-patch
tutor config save
```

## Configuration

You can customize the worker parameters in your Tutor config:

```yaml
# CMS Worker settings
CELERY_WORKER_PATCH_CMS_CONCURRENCY: 1
CELERY_WORKER_PATCH_CMS_MAX_TASKS_PER_CHILD: 100
CELERY_WORKER_PATCH_CMS_PREFETCH_MULTIPLIER: 1
CELERY_WORKER_PATCH_CMS_QUEUES: "edx.cms.core.default,edx.cms.core.high,edx.cms.core.low"

# LMS Worker settings
CELERY_WORKER_PATCH_LMS_CONCURRENCY: 1
CELERY_WORKER_PATCH_LMS_MAX_TASKS_PER_CHILD: 100
CELERY_WORKER_PATCH_LMS_PREFETCH_MULTIPLIER: 1
CELERY_WORKER_PATCH_LMS_QUEUES: "edx.lms.core.default,edx.lms.core.high,edx.lms.core.high_mem"
```

## Apply changes

After modifying configuration, regenerate the environment and restart:

```bash
tutor config save
tutor local restart  # or tutor k8s restart
```

## License

This software is licensed under the terms of the AGPLv3.
