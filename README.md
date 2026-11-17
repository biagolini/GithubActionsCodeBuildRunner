# GitHub Actions CodeBuild Runner

**Author:** Carlos Biagolini-Jr.

**LinkedIn:** https://www.linkedin.com/in/biagolini/

**Medium:** https://medium.com/@biagolini

**Companion article:** https://medium.com/@biagolini/79b533db9cdd

> **Didactic notice:** This project was developed as a practical example to accompany a blog post. The architecture decisions made here were chosen to meet an educational objective. They illustrate concepts clearly, not necessarily in the most production-ready way. Feel free to draw inspiration from these ideas, but remember to evaluate the limitations and constraints of your own business before adopting any of them. This project is released under the [MIT License](./LICENSE): you are free to copy, modify, and use it as you wish, but it comes with no warranties and the author takes no responsibility for its use in any environment.

## Overview

A GitHub Actions workflow that builds a multi-architecture container image (`amd64` and `arm64`) and pushes it to Amazon ECR, running every job on a serverless, ephemeral runner hosted by [AWS CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/action-runner-overview.html). Each architecture is built natively, without emulation, by overriding the image of the runner in the `runs-on` label. The sample application is a small Flask calculator (addition, subtraction, multiplication, and division) with an `/arch` endpoint that reports the CPU architecture it runs on.

The workflow has no `configure-aws-credentials` step and no AWS secret in GitHub. The AWS credentials come from the service role of the CodeBuild project, which is limited to pushing to one ECR repository.

## Prerequisites

- A **private** GitHub repository (use self-hosted runners only with private repositories, because forks of a public repository can run code on the runner).
- An AWS account with an Amazon ECR repository and a CodeBuild project named `github-runner-builds`, configured as a runner project for this repository with privileged mode enabled and a webhook for the `WORKFLOW_JOB_QUEUED` event.
- A service role for the project with permission to push to the ECR repository and to read the CodeConnections connection of the GitHub App.
- A CodeConnections connection to GitHub, set as the source credential of CodeBuild.

## Setup

1. Copy this repository into your private repository.

2. In the repository, open **Settings**, then **Secrets and variables**, then **Actions**, and create two variables:

- `AWS_REGION` with a Region such as `us-east-1`
- `ECR_REPOSITORY` with the name of your ECR repository

3. If your CodeBuild project has a different name, replace `github-runner-builds` in the `runs-on` lines of the workflow.

## Usage

To try the application locally, run `pip install -r requirements.txt` and `python -m src.app`, then open `http://localhost:8080/add/2/3` or `http://localhost:8080/arch`. In the pipeline, push to `main`, or run the workflow from the **Actions** tab. The `build (amd64)` and `build (arm64)` jobs run in parallel on two CodeBuild builds, and the `manifest` job joins both images in a manifest list under the tag of the commit.

## Project Structure

```
.
├── .github/workflows/
│   └── build-push-codebuild.yml   # build matrix on CodeBuild runners and manifest list
├── .gitignore
├── .vscode/settings.json
├── Dockerfile                     # Python image from ECR Public, no architecture named
├── LICENSE
├── README.md
├── requirements.txt               # Flask and Gunicorn
└── src/
    ├── __init__.py
    └── app.py                     # calculator endpoints and /arch
```

## Cleanup

Delete the CodeBuild project (which removes its webhook), the service role, the ECR repository, and the CodeConnections connection if you no longer need them.

## Contributing

Feel free to submit issues and pull requests.

## License

This project is open source and available under the [MIT License](LICENSE).
