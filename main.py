from flask import Flask, request, jsonify
import gitlab
import requests
import time
import json

app = Flask(__name__)

GITLAB_TOKEN = "YOUR_GITLAB_TOKEN"
SLACK_TOKEN = "YOUR_SLACK_BOT_TOKEN"
APP_PROJECT_ID = "YOUR_APP_PROJECT_ID"
KAIJU_PROJECT_ID = "YOUR_KAIJU_PROJECT_ID"
IZANAKI_PROJECT_ID = "YOUR_IZANAKI_PROJECT_ID"
GITLAB_URL = "https://gitlab.com"
SLACK_CHANNEL_ID = "YOUR_SLACK_CHANNEL_ID"

gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

def send_comical_message_to_slack(text, attachments=None):
    SLACK_API_URL = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    data = {
        "channel": SLACK_CHANNEL_ID,
        "text": text,
        "attachments": attachments
    }
    response = requests.post(SLACK_API_URL, headers=headers, json=data).json()
    return response.get('ts')

def update_slack_message(ts, text):
    SLACK_API_URL = "https://slack.com/api/chat.update"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    data = {
        "channel": SLACK_CHANNEL_ID,
        "text": text,
        "ts": ts
    }
    requests.post(SLACK_API_URL, headers=headers, json=data)

def create_branch(project_id, branch_name):
    project = gl.projects.get(project_id)
    try:
        branch = project.branches.create({'branch': branch_name, 'ref': 'master'})
        return True
    except Exception as e:
        print(f"Failed to create branch. Error: {str(e)}")
        return False

def get_pipeline_id(project_id, branch_name):
    project = gl.projects.get(project_id)
    pipelines = project.pipelines.list(ref=branch_name)
    if pipelines:
        return pipelines[0].id
    return None

def poll_for_pipeline_id(project_id, branch_name, timeout=300):
    start_time = time.time()

    while time.time() - start_time < timeout:
        pipeline_id = get_pipeline_id(project_id, branch_name)
        if pipeline_id:
            return pipeline_id
        time.sleep(10)

    return None

def poll_pipeline_status(project_id, pipeline_id, slack_msg_ts):
    project = gl.projects.get(project_id)
    progress = 0
    while progress < 100:
        pipeline = project.pipelines.get(pipeline_id)
        progress += 10
        progress_bar = "▓" * (progress // 10) + "░" * (10 - progress // 10)
        update_text = f"Pipeline Progress: [{progress_bar}] {progress}%"
        update_slack_message(slack_msg_ts, update_text)

        if pipeline.status in ['success', 'failed', 'canceled']:
            return pipeline.status == 'success'
        time.sleep(10)

def trigger_manual_jobs(project_id, pipeline_id):
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
    project = gl.projects.get(project_id)
    pipeline = project.pipelines.get(pipeline_id)
    jobs = pipeline.jobs.list()
    manual_job_names = ["manual_job_1", "manual_job_2"]
    
    for job in jobs:
        if job.name in manual_job_names:
            job.play()
    
    print(f"Manual jobs triggered for pipeline ID {pipeline_id}")

@app.route('/slack_command_endpoint', methods=['POST'])
def handle_slack_command():
    branch_name = request.form['text']
    
    # For App
    slack_msg_ts_app = send_comical_message_to_slack(f"APP: Summoning the magical branch {branch_name}... 🪄✨")
    time.sleep(2)
    create_branch_success_app = create_branch(APP_PROJECT_ID, branch_name)
    update_slack_message(slack_msg_ts_app, f"APP: Voila! The branch {branch_name} has blossomed! 🌳" if create_branch_success_app else f"APP: Oops! Branch {branch_name} creation failed. 🥀")
    
    # For Kaiju
    slack_msg_ts_kaiju = send_comical_message_to_slack(f"KAIJU: Summoning the magical branch {branch_name}... 🪄✨")
    time.sleep(2)
    create_branch_success_kaiju = create_branch(KAIJU_PROJECT_ID, branch_name)
    update_slack_message(slack_msg_ts_kaiju, f"KAIJU: Voila! The branch {branch_name} has blossomed! 🌳" if create_branch_success_kaiju else f"KAIJU: Oops! Branch {branch_name} creation failed. 🥀")
    
    if create_branch_success_app and create_branch_success_kaiju:
        pipeline_id_app = poll_for_pipeline_id(APP_PROJECT_ID, branch_name)
        pipeline_id_kaiju = poll_for_pipeline_id(KAIJU_PROJECT_ID, branch_name)

        if pipeline_id_app and pipeline_id_kaiju:
            slack_msg_ts_app_pipeline = send_comical_message_to_slack(f"APP: Setting up the magic trick for {branch_name}... 🪄✨")
            pipeline_success_app = poll_pipeline_status(APP_PROJECT_ID, pipeline_id_app, slack_msg_ts_app_pipeline)
            update_slack_message(slack_msg_ts_app_pipeline, f"APP: All magic tricks for {branch_name} completed! 🎩✨🎉" if pipeline_success_app else f"APP: Oops! The magic trick for {branch_name} failed.")

            slack_msg_ts_kaiju_pipeline = send_comical_message_to_slack(f"KAIJU: Setting up the magic trick for {branch_name}... 🪄✨")
            pipeline_success_kaiju = poll_pipeline_status(KAIJU_PROJECT_ID, pipeline_id_kaiju, slack_msg_ts_kaiju_pipeline)
            update_slack_message(slack_msg_ts_kaiju_pipeline, f"KAIJU: All magic tricks for {branch_name} completed! 🎩✨🎉" if pipeline_success_kaiju else f"KAIJU: Oops! The magic trick for {branch_name} failed.")
            
            # Trigger manual jobs in Izanaki
            trigger_manual_jobs(IZANAKI_PROJECT_ID, pipeline_id_kaiju)
        else:
            return jsonify(response_type='in_channel', text=f'Pipeline initialization failed for {"APP" if not pipeline_id_app else "KAIJU"}!')
    else:
        return jsonify(response_type='in_channel', text=f'Branch creation failed for {"APP" if not create_branch_success_app else "KAIJU"}!')

    return jsonify(response_type='in_channel', text=f'Branch created and magic tricks set up for {branch_name}!')

@app.route('/slack_button_endpoint', methods=['POST'])
def handle_slack_button_click():
    payload = json.loads(request.form['payload'])
    action = payload['actions'][0]['value']
    branch_name = payload['original_message']['text'].split("for ")[1].split("!")[0]

    # Define the base branch for Izanaki actions
    base_branch = "23.9"

    if action == "deploy_izanaki":
        slack_msg_ts_deploy_izanaki_pipeline = send_comical_message_to_slack(f"Izanaki: Setting up the magic trick for {branch_name}... 🪄✨")
        pipeline_id_deploy_izanaki = poll_for_izanaki_pipeline_id(branch_name)
        pipeline_success_deploy_izanaki = poll_izanaki_pipeline_status(IZANAKI_PROJECT_ID, pipeline_id_deploy_izanaki, slack_msg_ts_deploy_izanaki_pipeline)
        update_slack_message(slack_msg_ts_deploy_izanaki_pipeline, f"Izanaki: All magic tricks for {branch_name} completed! 🎩✨🎉" if pipeline_success_deploy_izanaki else f"Izanaki: Oops! The magic trick for {branch_name} failed.")
        
        # Trigger manual jobs in Izanaki
        trigger_manual_jobs(IZANAKI_PROJECT_ID, pipeline_id_deploy_izanaki)
        
    elif action == "staging_izanaki":
        slack_msg_ts_staging_izanaki_pipeline = send_comical_message_to_slack(f"Izanaki: Setting up the magic trick for {branch_name}... 🪄✨")
        pipeline_id_staging_izanaki = poll_for_izanaki_pipeline_id(branch_name)
        pipeline_success_staging_izanaki = poll_izanaki_pipeline_status(IZANAKI_PROJECT_ID, pipeline_id_staging_izanaki, slack_msg_ts_staging_izanaki_pipeline)
        update_slack_message(slack_msg_ts_staging_izanaki_pipeline, f"Izanaki: All magic tricks for {branch_name} completed! 🎩✨🎉" if pipeline_success_staging_izanaki else f"Izanaki: Oops! The magic trick for {branch_name} failed.")
        
        # Trigger manual jobs in Izanaki
        trigger_manual_jobs(IZANAKI_PROJECT_ID, pipeline_id_staging_izanaki)
        
    elif action == "tag_izanaki":
        slack_msg_ts_tag_izanaki = send_comical_message_to_slack(f"Izanaki: Creating tag for {branch_name}... 🏷️")
        create_tag_success_izanaki = create_izanaki_tag(branch_name, base_branch)
        update_slack_message(slack_msg_ts_tag_izanaki, f"Izanaki: Tag for {branch_name} created! 🏷️" if create_tag_success_izanaki else f"Izanaki: Oops! Tag creation for {branch_name} failed.")

    return jsonify(response_type='in_channel', text=f'Performing action: {action} for {branch_name}')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
