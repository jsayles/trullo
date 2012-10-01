
var schema = schema || {};

schema.initialCap = function(str){
	return str.substring(0, 1).toUpperCase() + str.substring(1)
}

schema.javascriptifyResourceName = function(resourceName){
	var result = schema.initialCap(resourceName);
	while(result.indexOf('-') != -1){
		var index = result.indexOf('-');
		result = result.substring(0, index) + schema.initialCap(result.substring(index + 1));
	}
	return result;
}

schema.hostNameFromURL = function(url){
	var splitURL = url.split('/');
	return splitURL[2];
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
		console.log(this.attributes);
		for(var name in this.attributes){
			var resourceClassName = schema.javascriptifyResourceName(name);
			schema[resourceClassName] = schema.AbstractTastyPieModel.extend({
				list_endpoint: this.attributes[name].list_endpoint,
			});
			schema[resourceClassName + 'Collection'] = schema.AbstractTastyPieCollection.extend({
				list_endpoint: this.attributes[name].list_endpoint,
				model: schema[resourceClassName],
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

var views = views || {};

views.AbstractCollectionView = Backbone.View.extend({
	tagName: 'section',
	initialize: function(){
		_.bindAll(this, 'render', 'add', 'remove', 'reset');
		this.$el.addClass('collection-view');
		this.itemViews = [];

		this.collection.on('add', this.add);
		this.collection.on('remove', this.remove);
		this.collection.on('reset', this.reset);
	},
	reset: function(){
		for(var i=0; i < this.collection.length; i++){
			this.add(this.collection.at(i));
		}
	},
	add: function(item){
		if(this.options.filter){
			var filterName = this.options.filter[0];
			var filterTargetValue = this.options.filter[1];
			var val = item.get(filterName, null);
			if(val != filterTargetValue) return;
		}
		if(this.options.mustBeSet){
			for(var i=0; i < this.options.mustBeSet.length; i++){
				var val = item.get(this.options.mustBeSet[i], null);
				if(val == null || val == '') return;
			}
		}
		this.itemViews[this.itemViews.length] = new this.itemView({model:item});
		this.$el.find('ul').append(this.itemViews[this.itemViews.length - 1].render().el);
	},
	remove: function(idea){
		console.log('remove', arguments);
	},
	render: function(){
		this.$el.empty();
		if(this.options.title) this.$el.append($.el.h1(this.options.title));
		this.$el.append($.el.ul());
		return this;
	},
})

views.AbstractItemView = Backbone.View.extend({
	tagName: 'li',
	initialize: function(){
		_.bindAll(this, 'render');
		this.$el.addClass('item-view');
		if(this.options.additionalClasses){
			for(var i=0; i < this.options.additionalClasses.length; i++){
				this.$el.addClass(this.options.additionalClasses);
			}
		}
	},
});


/*
Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) 
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/