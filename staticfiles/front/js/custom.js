/*
  Version: 1.0
  Author: BanyanTheme
  Website: https://banyanthemes.com/
*/

(function($) {
 
 	"use strict"; 
    $(document).ready(function(){

		// Page preloader
		$("#fakeloader").fakeLoader({
			timeToHide:1000,
			zIndex:"999999",//Default zIndex
			bgColor:"#ffffff",
			spinner:"spinner1"
		});	
		
		// show body after site load
		$('body').show();


        /*mag popup*/       
        $('.video').magnificPopup({
          type: 'iframe',


          iframe: {
             markup: '<div class="mfp-iframe-scaler">'+
                        '<div class="mfp-close"></div>'+
                        '<iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>'+
                        '<div class="mfp-title">Some caption</div>'+
                      '</div>'
          },
          callbacks: {
            markupParse: function(template, values, item) {
             values.title = item.el.attr('title');
            }
          }

        }); 

		//Testimonial Carousel (Slick) 
		  $('.testimonial').slick({
		    	slidesToShow: 1,
			    slidesToScroll: 1,
			    autoplay: true,
	  			autoplaySpeed: 3000,
			    arrows: true,
			    nextArrow: '<i class="fas fa-angle-right"></i>',
  				prevArrow: '<i class="fas fa-angle-left"></i>',
			    focusOnSelect: true,
			    easing: 'linear'
		  });               
 
		//learning-path Carousel (Slick) 
		  $('.learning-path').slick({
		    	slidesToShow: 4,
			    slidesToScroll: 1,
			    autoplay: true,
	  			autoplaySpeed: 3000,
			    arrows: true,
			    nextArrow: '<i class="fas fa-angle-right"></i>',
  				prevArrow: '<i class="fas fa-angle-left"></i>',
			    focusOnSelect: true,
			    easing: 'linear',
			    responsive: [
				    {
				      breakpoint: 768,
				      settings: {
				        slidesToShow: 2,
				        slidesToScroll: 3,
				        infinite: true
				      }
				    },
				    {
				      breakpoint: 480,
				      settings: {
				        slidesToShow: 1,
				        slidesToScroll: 1
				      }
				    }
				  ]
		  }); 

		//Related Course Slider (Slick) 
		  $('.related-course').slick({
		    	slidesToShow: 4,
			    slidesToScroll: 1,
			    autoplay: true,
	  			autoplaySpeed: 3000,
			    arrows: true,
			    nextArrow: '<i class="fas fa-angle-right"></i>',
  				prevArrow: '<i class="fas fa-angle-left"></i>',
			    focusOnSelect: true,
			    easing: 'linear',
			    responsive: [
				    {
				      breakpoint: 768,
				      settings: {
				        slidesToShow: 2,
				        slidesToScroll: 2,
				        infinite: true
				      }
				    },
				    {
				      breakpoint: 480,
				      settings: {
				        slidesToShow: 1,
				        slidesToScroll: 1
				      }
				    }
				  ]
		  }); 
        //counter
		$('.counter').counterUp({
			delay: 10,
			time: 5000
		});
                		
		// Masonry portfolio
		$('.all-course').mixItUp({
			selectors: {
				target: '.tile',
				filter: '.filter',
				sort: '.sort-btn'
			},		  
			animation: {
			animateResizeContainer: false,
			effects: 'fade scale'
			}
		});

		// Initilize wow js
		new WOW().init();    



  }); // End load document
 
})(jQuery);