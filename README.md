# README for Flask-GitLab-Slack Integration

This project is a Flask application designed to create GitLab branches and monitor GitLab CI/CD pipeline progress, with updates sent to a Slack channel. It facilitates the interaction between Slack commands and GitLab CI/CD, allowing users to trigger pipelines and manual jobs directly from Slack.

## Features

- Create new GitLab branches via Slack commands.
- Monitor the progress of GitLab CI/CD pipelines in Slack.
- Trigger manual GitLab pipeline jobs from Slack.
- Integration with multiple GitLab projects.
- Updates and notifications are sent to a designated Slack channel.

## Requirements

- Python 3.6 or higher
- Flask
- GitLab account with API access
- Slack workspace with a bot token

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/your-repository.git
```

2. Navigate to the cloned directory:

```bash
cd your-repository
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

Configure the following environment variables with your GitLab and Slack credentials:

- `GITLAB_TOKEN`: Your GitLab API token.
- `SLACK_TOKEN`: Your Slack bot token.
- `APP_PROJECT_ID`: The ID of your GitLab project for the "App".
- `KAIJU_PROJECT_ID`: The ID of your GitLab project for "Kaiju".
- `IZANAKI_PROJECT_ID`: The ID of your GitLab project for "Izanaki".
- `SLACK_CHANNEL_ID`: The ID of your Slack channel where messages will be sent.

Set these variables in your environment, or include them in a `.env` file in your project's root directory (and use a package like `python-dotenv` to load them).

## Running the Application

To run the Flask application:

```bash
flask run --host=0.0.0.0 --port=5000
```

The app will start on port 5000 and will be accessible from your network.

## Local Testing

For local testing, you can use tools like [ngrok](https://ngrok.com/) to expose your local server to the internet.

1. Start ngrok on the same port as your Flask app:

```bash
ngrok http 5000
```

2. Copy the ngrok URL (e.g., `https://12345.ngrok.io`) and use it to configure the Slack command and interactive message endpoints.

### Slack Integration for Local Testing

- Update your Slack app's Slash Commands and interactive components with the ngrok URL.
- For Slash Commands, append `/slack_command_endpoint` to the ngrok URL.
- For interactive components, append `/slack_button_endpoint` to the ngrok URL.

After setting up ngrok, you can interact with your Flask application through Slack as if it were deployed on a server.
