var trullo = trullo || {};
trullo.views = trullo.views || {};

trullo.views.IndexView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
		this.logEntries = new schema.LogEntryCollection();
		this.logEntriesView = new publish.views.LogEntryCollectionView({collection:this.logEntries, filter:['source_url', null]});
		this.logEntriesView.$el.addClass('span6');
		this.streamView = new publish.views.LogEntryCollectionView({collection:this.logEntries, mustBeSet:['source_url']});
		this.streamView.$el.addClass('span6');
		this.logEntries.fetch();
	},
	render: function(){
		this.$el.empty();
		var row1 = $.el.div({class:'row-fluid'});
		this.$el.append(row1);
		row1.append(this.logEntriesView.render().el);
		row1.append(this.streamView.render().el);
		return this;
	},
});

trullo.views.AboutView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
	},
	render: function(){
		this.$el.append($.el.h1('About'));
		return this;
	},
});

trullo.views.ContactView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
	},
	render: function(){
		this.$el.append($.el.h1('Contact'));
		return this;
	},
});
