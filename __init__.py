"""
Trullo is a Django project which provides a creative, maker type person with a vanity site.
It includes project tracking, idea collection, and a web logging facility.
"""
from tastypie.api import Api
API = Api(api_name='v0.1')

from publish.api import LogEntryResource
from front.api import UserResource

# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
