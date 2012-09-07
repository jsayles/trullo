var publish = publish || {};
publish.views = publish.views || {};

publish.views.AbstractCollectionView = Backbone.View.extend({
	tagName: 'ul',
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
		this.itemViews[this.itemViews.length] = new this.itemView({model:item});
		this.$el.append(this.itemViews[this.itemViews.length - 1].render().el);
	},
	remove: function(idea){
		console.log('remove', arguments);
	},
	render: function(){
		return this;
	},
})

publish.views.AbstractItemView = Backbone.View.extend({
	tagName: 'li',
	initialize: function(){
		_.bindAll(this, 'render');
		this.$el.addClass('item-view');
	},
});

publish.views.IdeaItemView = publish.views.AbstractItemView.extend({
	className: 'idea-item-view',
	render: function(){
		this.$el.append($.el.h3(this.model.get('title')));
		return this;
	},
});

publish.views.IdeaCollectionView = publish.views.AbstractCollectionView.extend({
	className: 'idea-collection-view',
	itemView: publish.views.IdeaItemView,
});

publish.views.ProjectItemView = publish.views.AbstractItemView.extend({
	className: 'project-item-view',
	render: function(){
		this.$el.append($.el.h3(this.model.get('title')));
		return this;
	},
});

publish.views.ProjectCollectionView = publish.views.AbstractCollectionView.extend({
	className: 'project-collection-view',
	itemView: publish.views.ProjectItemView,
});
