var redraw;
var height = 300;
var width = 400;

/* only do all this when document has finished loading (needed for RaphaelJS */
$(function() {
	$.get('/factopy/api/v1/stream/?format=json', 'json', function(data){
	    var g = new Graph();
		streams = data.objects;
		targets = {};
		for (var i = 0; i < streams.length; i++) {
			t = streams[i];
			target = t.feed.name + ' ['+ t.unprocessed_count +']';
			targets[t.feed.name] = target;
			for (var j = 0; j < t.observe.length; j++) {
				s = t.observe[j];
				source = targets[s.name];
				g.addEdge(source, target);
			}
		}

	    /* layout the graph using the Spring layout implementation */
	    var layouter = new Graph.Layout.Spring(g);
	    layouter.layout();
    
	    /* draw the graph using the RaphaelJS draw implementation */
	    var renderer = new Graph.Renderer.Raphael('canvas', g, width, height);
	    renderer.draw();
    
	    redraw = function() {
	        layouter.layout();
	        renderer.draw();
	    };
	});
});
