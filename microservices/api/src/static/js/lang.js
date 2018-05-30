var twoColComp = {
  init: function() {
    var tables = document.getElementsByTagName('table');

    // for each table
    for (var i = 0; i < tables.length; i++) {
      // don't process one that's already been done (has class two-column-comp)
      if (new RegExp('(^| )two-column-comp( |$)', 'gi').test(tables[i].className)) {
        return;
      }

      //TODO: need to verify cross-browser support of these vars
      var h = tables[i].clientHeight,
        t = tables[i].getBoundingClientRect().top,
        wT = window.pageYOffset || document.documentElement.scrollTop,
        wH = window.innerHeight;

      if (wT + wH > t + h / 2) {
        this.make(tables[i]);
      }
    }
  },

  make: function(el) {
      var rows = el.getElementsByTagName('tr'),
        vals = [],
        max,
        percent;

      // for each row in the table, get vals
      for (var x = 0; x < rows.length; x++) {
        var cells = rows[x].getElementsByTagName('td');
        for (var y = 1; y < cells.length; y++) {
          vals.push(parseInt(cells[y].innerHTML, 10));
        }
      }

      max = Math.max.apply(Math, vals);
      percent = 100 / max;

      //for each row in the table, apply vals
      for (x = 0; x < rows.length; x++) {
        var cells = rows[x].getElementsByTagName('td');
        for (var y = 1; y < cells.length; y++) {
          var currNum = parseInt(cells[y].innerHTML, 10);
          cells[y].style.backgroundSize = percent * currNum + "% 100%";
          cells[y].style.transitionDelay = x / 20 + "s";
        }
      }
      //add a class so you don't process it a bunch of times
      el.className = +" two-column-comp"
    } // end make
}

window.onload = function() {
  twoColComp.init();
}

window.onscroll = function() {
  twoColComp.init();
}