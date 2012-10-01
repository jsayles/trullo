
var schema = schema || {};

schema.initialCap = function(str){
	return str.substring(0, 1).toUpperCase() + str.substring(1);
}

schema.AbstractTastyPieModel = Backbone.Model.extend({
	url: function(){
		if(typeof this.get('id') == 'undefined') return this.list_endpoint;
		return this.list_endpoint + this.get('id');
	}, 
});

schema.AbstractTastyPieCollection = Backbone.Collection.extend({
	url: function(){ return this.list_endpoint; }, 
});

schema.TastyPieSchema = Backbone.Model.extend({
	url: '/api/publish/v0.1/',
	populate: function(){
		for(var name in this.attributes){
			schema[schema.initialCap(name)] = schema.AbstractTastyPieModel.extend({
				list_endpoint: this.attributes[name].list_endpoint,
			});
			schema[schema.initialCap(name) + 'Collection'] = schema.AbstractTastyPieCollection.extend({
				list_endpoint: this.attributes[name].list_endpoint,
				model: schema[schema.initialCap(name)],
			});
		}
		this.trigger('populated', this);
	}
});

schema.tastyPieSchema = new schema.TastyPieSchema();

schema.parseJsonDate = function(jsonDate){
    var dateString = jsonDate.split('T')[0];
    var dateArray = dateString.split('-');
    var date = new Date(dateArray[1] + ' ' + dateArray[2] + ' ' + dateArray[0]);
    var timeArray = jsonDate.split('T')[1].split(':');
    return new Date(date.getFullYear(), date.getMonth(), date.getDate(), parseInt(timeArray[0], 10), parseInt(timeArray[1], 10), parseInt(timeArray[2], 10));
}

schema.formatDate = function(jsDate){
	return schema.MONTH_STRINGS[jsDate.getMonth()] + ' ' + jsDate.getDate() + ', ' + jsDate.getFullYear();
}

schema.MONTH_STRINGS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

$(document).ready(function(){
	schema.tastyPieSchema.fetch({success: function(){
		schema.tastyPieSchema.populate();
	}});
});

/*
Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) 
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/