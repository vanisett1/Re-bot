# SlyncOps

# Flask-GitLab-Slack Integration

This project is a Flask application designed to create GitLab branches and monitor GitLab CI/CD pipeline progress, with updates sent to a Slack channel. It also allows triggering manual jobs in a GitLab pipeline via Slack commands.

## Features

- Creation of new branches in GitLab from a Slack command.
- Monitoring the progress of GitLab CI/CD pipelines in Slack.
- Triggering manual jobs in GitLab pipelines from Slack.
- Integration with multiple GitLab projects.
- Sending updates and notifications to a designated Slack channel.

## Requirements

- Python 3.6 or higher
- Flask
- GitLab account with API access
- Slack workspace with a bot token

## Installation

1. Clone the repository to your local machine.

```bash
git clone https://github.com/your-username/your-repository.git
```

2. Navigate to the cloned directory.

```bash
cd your-repository
```

3. Install the required Python packages.

```bash
pip install -r requirements.txt
```

## Configuration

You must set the following environment variables with your GitLab and Slack credentials:

- `GITLAB_TOKEN`: Your GitLab API token.
- `SLACK_TOKEN`: Your Slack bot token.
- `APP_PROJECT_ID`: The ID of your GitLab project for the "App".
- `KAIJU_PROJECT_ID`: The ID of your GitLab project for "Kaiju".
- `IZANAKI_PROJECT_ID`: The ID of your GitLab project for "Izanaki".
- `SLACK_CHANNEL_ID`: The ID of your Slack channel where messages will be sent.

You can set these variables in your environment, or you can directly replace the placeholder strings in the code with your actual credentials (not recommended for security reasons).

## Running the Application

Run the Flask application by executing the following command:

```bash
flask run --host=0.0.0.0 --port=5000
```

The application will start on port 5000 and will be accessible from your network.

## Usage

- To create a branch and start pipelines, send a Slack command with the branch name.
- To check the pipeline status or trigger manual jobs, use the corresponding Slack commands that interact with this Flask application.

## Slack Integration

You must set up Slash Commands and interactive components in your Slack app to interact with this Flask application.

- For Slash Commands, point to the `/slack_command_endpoint` endpoint of your application.
- For interactive components (like buttons), point to the `/slack_button_endpoint` endpoint.


