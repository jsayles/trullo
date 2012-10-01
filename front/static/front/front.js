var trullo = trullo || {};
trullo.views = trullo.views || {};

trullo.views.IndexView = Backbone.View.extend({
	className: 'routeView',
	initialize: function(){
		_.bindAll(this, 'render');
	},
	render: function(){
		this.$el.append($.el.h1('News'));
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
