var trullo = trullo || {};
trullo.views = trullo.views || {};

trullo.views.IndexView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
		this.logEntries = new schema.LogEntryCollection([], {limit: 10, filters:{'source_url__isnull':'True'}});
		this.logEntriesView = new publish.views.LogEntryCollectionView({collection:this.logEntries});
		this.logEntriesView.$el.addClass('span6');
		this.logEntries.fetch();

		this.streamEntries = new schema.LogEntryCollection([], {limit: 10, filters:{'source_url__isnull':'False'}});
		this.streamView = new publish.views.LogEntryCollectionView({collection:this.streamEntries});
		this.streamView.$el.addClass('span6');
		this.streamEntries.fetch();
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
