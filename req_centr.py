import requests
from ImageCloud import save_image_to_gcs, sample_base64_image

class RestBai:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_endpoint = "https://api-eu.restb.ai/vision/v2/multipredict"
        self.json_response = None
        self.rb_classes = {}
        self.im_width = 1280
        self.im_height = 960

    def response(self, img64, model_id = "re_features_v4"):
        #Transform the image from base64 to URL
        image_url, self.im_width, self.im_height = save_image_to_gcs(img64)
        image_url = "https://www.digitaltveurope.com/files/2020/11/Walmart-TV-department.jpg"
        # create a dictionary with the request parameters
        payload = {
            "client_key": self.api_key,
            "model_id": model_id,
            "image_url": image_url
        }

        # send a GET request to the API endpoint with the request parameters
        response = requests.get(self.api_endpoint, params=payload)

        # parse the JSON response
        self.json_response = response.json()

        # return the labels
        return self.json_response

    def return_classes(self):
        self.classes = {}
        # return the classes
        # {'error': 'false', 'response': {'solutions': {'re_features_v4': {'detections': [{'details': [], 'label': 'tv'}, {'details': [], 'label': 'built_in_shelves'}, {'details': [], 'label': 'beamed_ceiling'}, {'details': [], 'label': 'coffered_ceiling'}, {'details': [], 'label': 'natural_light'}, {'details': [], 'label': 'fireplace'}, {'details': [{'label': 'dark'}], 'label': 'hardwood_floor'}]}}}, 'time': '2023-05-12T23:13:37.276101', 'correlation_id': '5eac8d67-b889-442f-b6ec-19e80520ef6a', 'version': '2'}
        for label in self.json_response["response"]["solutions"][model_id]["detections"]:
            # print(label["label"])
            # {'detections': [{'center_point': {'x': 0.875, 'y': 0.8984375}, 'details': [{'label': 'dark'}], 'label': 'hardwood_floor'}, {'center_point': {'x': 0.390625, 'y': 0.984375}, 'details': [{'label': 'dark'}], 'label': 'hardwood_floor'}, {'center_point': {'x': 0.546875, 'y': 0.248046875}, 'details': [], 'label': 'coffered_ceiling'}, {'center_point': {'x': 0.625, 'y': 0.1953125}, 'details': [], 'label': 'beamed_ceiling'}, {'center_point': {'x': 0.1484375, 'y': 0.3984375}, 'details': [], 'label': 'built_in_shelves'}, {'center_point': {'x': 0.29851973684210525, 'y': 0.37253289473684215},
            center = label['center_point']
            coordinates = [center.get('x') * self.im_width, center.get('y') * self.im_height]
            if label["label"] in self.classes:
                self.classes[label["label"]].append(coordinates)
            else:
                self.classes[label["label"]] = [coordinates]
        return self.classes
        
    def _filter_classes(self, ):
        pass

# Define API key
api_key = os.environ.get("RESTBAI")

# create a RestBai instance with your API key
restbai = RestBai(api_key)

# specify the image URL you want to classify and the model ID to use
image_64 = sample_base64_image

model_id = "re_features_v4"

# classify the image and print the result
result = restbai.response(image_64, model_id = "re_features_v4")
print(result)

# return the classes
classes = restbai.return_classes()
print(classes)