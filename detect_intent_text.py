#!/usr/bin/env python

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
projects/hallowed-air-224411/locations/global/agents/8cea499e-ab26-42c8-af20-a5d9c084748e

To start conversation

python detect_intent_text.py --session-id '07cc785c-d514-425f-9b43-451715c8ea7d' "hi" "yupp" "i need butter toast and boiled eggs"

"""

import uuid
import argparse
import os
from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session

#google cloud service account key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'hallowed-air-224411-3da7b64e0cec.json'

# [START dialogflow_detect_intent_text]
def run_sample(sessionid,query):
    # TODO(developer): Replace these values when running the function
    project_id = "hallowed-air-224411"
    # For more information about regionalization see https://cloud.google.com/dialogflow/cx/docs/how/region
    location_id = "global"
    # For more info on agents see https://cloud.google.com/dialogflow/cx/docs/concept/agent
    agent_id = "8cea499e-ab26-42c8-af20-a5d9c084748e"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    # For more information on sessions see https://cloud.google.com/dialogflow/cx/docs/concept/session
    #session_id = uuid.uuid4()
    session_id = sessionid
    texts = query
    # For more supported languages see https://cloud.google.com/dialogflow/es/docs/reference/language
    language_code = "en-us"
    detect_intent_texts(agent, session_id, texts, language_code)


def detect_intent_texts(agent, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")
    client_options = None
    agent_components = AgentsClient.parse_agent_path(agent)
    location_id = agent_components["location"]
    if location_id == "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    for text in texts:
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=language_code)
        request = session.DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")


# [END dialogflow_detect_intent_text]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--session-id", help="Identifier of the DetectIntent session. " "Defaults to a random UUID.", default=str(uuid.uuid4()))
    parser.add_argument("texts", nargs="+", type=str, help="Text inputs.")
    args = parser.parse_args()
    run_sample(args.session_id,args.texts)