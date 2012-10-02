var publish = publish || {};
publish.views = publish.views || {};

publish.views.LogEntryItemView = views.AbstractItemView.extend({
	className: 'log-entry-view',
	render: function(){
		this.$el.append($.el.h3($.el.a({href:this.model.get('absolute_url')}, this.model.get('subject'))));
		if(this.model.get('source_url')){
			this.$el.append($.el.p(schema.hostNameFromURL(this.model.get('source_url'))));
		}
		return this;
	},
});

publish.views.LogEntryCollectionView = views.AbstractCollectionView.extend({
	className: 'log-entry-collection-view',
	itemView: publish.views.LogEntryItemView,
});

publish.views.IdeaItemView = views.AbstractItemView.extend({
	className: 'idea-item-view',
	render: function(){
		this.$el.append($('<h3 />').html(this.model.get('title')));
		this.$el.append($('<p />').html(this.model.get('description')));
		return this;
	},
});

publish.views.IdeaCollectionView = views.AbstractCollectionView.extend({
	className: 'idea-collection-view',
	itemView: publish.views.IdeaItemView,
});

publish.views.ProjectItemView = views.AbstractItemView.extend({
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

publish.views.ProjectCollectionView = views.AbstractCollectionView.extend({
	className: 'project-collection-view',
	itemView: publish.views.ProjectItemView,
});

publish.views.ProjectsView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
		this.projectCollection = new schema.ProjectCollection({limit:1000});
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

publish.views.PublicationItemView = views.AbstractItemView.extend({
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

publish.views.PublicationCollectionView = views.AbstractCollectionView.extend({
	className: 'publication-collection-view',
	itemView: publish.views.PublicationItemView,
});

publish.views.PublicationsView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
		this.collection = new schema.PublicationCollection({limit:1000});
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
