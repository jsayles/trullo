var trullo = trullo || {};
trullo.views = trullo.views || {};

trullo.Router = Backbone.Router.extend({
	routes: {
		"":"home",
		"about":"about",
	},
	home: function(){
		trullo.activateNav('#');
		$('.routeView').hide();
		$('#homeView').show();
	},

	about: function() {
		trullo.activateNav('#about');
		$('.routeView').hide();
		$('#aboutView').show();
	},
});
window.router = new trullo.Router();

trullo.activateNav = function(hash){
	$('.nav li').attr('class', 'inactive');
	$('a[href=' + hash + ']').parent().attr('class', 'active');
}

trullo.views.PageView = Backbone.View.extend({
	id: 'pageView',

	initialize: function(){
		this.aboutView = new trullo.views.AboutView();
		this.$el.append(this.aboutView.render().el);
		this.homeView = new trullo.views.HomeView();
		this.$el.append(this.homeView.render().el);
	},

	render: function(){
		return this;
	},
});

trullo.views.HomeView = Backbone.View.extend({
	className: 'routeView',
	id: 'homeView',
	initialize: function(){
		_.bindAll(this, 'render');
		this.projectCollection = new schema.ProjectCollection();
		this.projectCollectionView = new publish.views.ProjectCollectionView({collection:this.projectCollection})
		this.projectCollection.fetch();

		this.ideaCollection = new schema.IdeaCollection();
		this.ideaCollectionView = new publish.views.IdeaCollectionView({collection:this.ideaCollection})
		this.ideaCollection.fetch();
	},
	render: function(){
		this.$el.append($.el.h1('Home:'));
		this.$el.append(this.projectCollectionView.render().el);
		this.$el.append(this.ideaCollectionView.render().el);
		return this;
	},
});

trullo.views.AboutView = Backbone.View.extend({
	className: 'routeView',
	id: 'aboutView',
	initialize: function(){
		_.bindAll(this, 'render');
	},
	render: function(){
		this.$el.append($.el.h1('About:'));
		return this;
	},
});

schema.tastyPieSchema.on('populated', function(){
	window.pageView = new trullo.views.PageView({el:$('#pageView')});
	window.pageView.render();
	Backbone.history.start();
	console.log('started');
});
