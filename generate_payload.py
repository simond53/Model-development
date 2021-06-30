import sys
import os
from ibm_watson_machine_learning import APIClient
import time


def generate_dict_payload():

    sample_payload = [3.0, 1.0, 1180.0, 5650.0, 1.0, 0.0, 0.0, 3.0, 7.0, 1180.0, 0.0, 1955.0, 0.0, 47.5112, -122.257, 1340.0, 5650.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    columns = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'lat', 'long', 'sqft_living15', 'sqft_lot15', '98001', '98002', '98003', '98004', '98005', '98006', '98007', '98008', '98010', '98011', '98014', '98019', '98022', '98023', '98024', '98027', '98028', '98029', '98030', '98031', '98032', '98033', '98034', '98038', '98039', '98040', '98042', '98045', '98052', '98053', '98055', '98056', '98058', '98059', '98065', '98070', '98072', '98074', '98075', '98077', '98092', '98102', '98103', '98105', '98106', '98107', '98108', '98109', '98112', '98115', '98116', '98117', '98118', '98119', '98122', '98125', '98126', '98133', '98136', '98144', '98146', '98148', '98155', '98166', '98168', '98177', '98178', '98188', '98198', '98199']

    # TODO take the mean values of the bedrooms, bathrooms etc. depending on the mean value of the selected zipcode 
    payload = {col : values for col,values in zip(columns, sample_payload)}

    return payload


# TODO coordinate with Austin for the payload 
def input_values(payload, zip_code):
    
    # We don't want to add new keys to the dictionary
    if zip_code in list(payload.keys()):
        payload[zip_code] = 1.0

    return payload


def format_payload(payload):
    formatted_payload = {'input_data': [{'values': [list(payload.values())]}]}
    return formatted_payload


def init_wml_client():

    WML_CREDENTIALS = {}
    WML_CREDENTIALS["url"] = "https://us-south.ml.cloud.ibm.com"

    wml_credentials = {
                    "url": WML_CREDENTIALS.get("url"),
                    "apikey": os.environ["api_key"]
                    }

    wml_client = APIClient(wml_credentials)

    return wml_client


def get_deployment_id(wml_client):

    DEPLOYMENT_NAME = 'House price prediction v1'
    deployment_details = wml_client.deployments.get_details()

    for deployment in deployment_details['resources']:

        deployment_id = deployment['metadata']['id']
        model_id = deployment['entity']['asset']['id']

        if deployment['entity']['name'] == DEPLOYMENT_NAME:
            print('Deleting deployment id', deployment_id)
            wml_client.deployments.delete(deployment_id)
            time.sleep(10)
            print('Deleting model id', model_id)
            wml_client.repository.delete(model_id)

    return deployment_id


def score_model(wml_client, deployment_id, formatted_payload):
    deployment_id = get_deployment_id(wml_client)
    wml_client.deployments.score(deployment_id, formatted_payload)


if __name__ == "__main__":

    #zip_code = sys.argv[1]
    #payload = generate_dict_payload()
    #payload = input_values(payload, zip_code)
    #formatted_payload = format_payload(payload)

    # TODO call the API
    wml_client = init_wml_client()
    
    score_model()





