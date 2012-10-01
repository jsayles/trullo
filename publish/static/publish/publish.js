var publish = publish || {};
publish.views = publish.views || {};

publish.views.AbstractCollectionView = Backbone.View.extend({
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

publish.views.AbstractItemView = Backbone.View.extend({
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

publish.views.IdeaItemView = publish.views.AbstractItemView.extend({
	className: 'idea-item-view',
	render: function(){
		this.$el.append($('<h3 />').html(this.model.get('title')));
		this.$el.append($('<p />').html(this.model.get('description')));
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
		if(this.model.get('url')){
			var title = $.el.h3();
			this.$el.append(title);
			var anchor = title.append($.el.a({href:this.model.get('url')}));
			$(anchor).html(this.model.get('title'));
		} else {
			this.$el.append($('<h3 />').html(this.model.get('title')));
		}
		this.$el.append($('<p />').html(this.model.get('description')));
		return this;
	},
});

publish.views.ProjectCollectionView = publish.views.AbstractCollectionView.extend({
	className: 'project-collection-view',
	itemView: publish.views.ProjectItemView,
});

publish.views.ProjectsView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
		this.projectCollection = new schema.ProjectCollection();
		this.portfolioCollectionView = new publish.views.ProjectCollectionView({collection:this.projectCollection, filter:['portfolio', true]})
		this.portfolioCollectionView.$el.addClass('span6');
		this.projectCollectionView = new publish.views.ProjectCollectionView({collection:this.projectCollection, filter:['portfolio', false]})
		this.projectCollectionView.$el.addClass('span6');
		this.projectCollection.fetch();
	},
	render: function(){
		var row1 = $.el.div({class:'row-fluid'});
		this.$el.append(row1);
		row1.append(this.portfolioCollectionView.render().el);
		row1.append(this.projectCollectionView.render().el);
		return this;
	},
});

publish.views.PublicationItemView = publish.views.AbstractItemView.extend({
	className: 'publication-item-view',
	render: function(){
		this.$el.append($('<h3 />').html('"' + this.model.get('title') + '"'));
		this.$el.append($.el.p(this.model.get('authors'), '.'));
		var publicationDate = schema.parseJsonDate(this.model.get('publication_date'));
		this.$el.append($.el.p(this.model.get('venue'), '. ', schema.formatDate(publicationDate), '.'));
		if(this.model.get('document')){
			this.$el.append($.el.a({href:this.model.get('document')}, 'download'))
		}
		if(this.model.get('source_url')){
			this.$el.append($.el.a({href:this.model.get('source_url')}, 'source'))
		}
		return this;
	},
});

publish.views.PublicationCollectionView = publish.views.AbstractCollectionView.extend({
	className: 'publication-collection-view',
	itemView: publish.views.PublicationItemView,
});

publish.views.PublicationsView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
		this.collection = new schema.PublicationCollection();
		this.collectionView = new publish.views.PublicationCollectionView({collection:this.collection});
		this.collectionView.$el.addClass('span12');
		this.collection.fetch();
	},
	render: function(){
		var row1 = $.el.div({class:'row-fluid'});
		this.$el.append(row1);
		row1.append(this.collectionView.render().el);
		return this;
	},
});
