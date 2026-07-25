// Make the five sidebar section headers (Furo `.caption`) collapsible.
// Each caption toggles the <ul> that follows it; the open/closed state is
// remembered per section across pages via localStorage.
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var tree = document.querySelector(".sidebar-tree");
    if (!tree) return;

    var captions = tree.querySelectorAll("p.caption");
    captions.forEach(function (caption, index) {
      var list = caption.nextElementSibling;
      if (!list || list.tagName !== "UL") return;

      caption.classList.add("caption-collapsible");
      caption.setAttribute("role", "button");
      caption.setAttribute("tabindex", "0");

      var label = (caption.textContent || String(index)).trim();
      var key = "binomcikit:sidebar:" + label;

      if (localStorage.getItem(key) === "collapsed") {
        caption.classList.add("collapsed");
        list.classList.add("caption-hidden");
      }

      function toggle() {
        var collapsed = caption.classList.toggle("collapsed");
        list.classList.toggle("caption-hidden", collapsed);
        try {
          localStorage.setItem(key, collapsed ? "collapsed" : "open");
        } catch (e) {
          /* storage may be unavailable (private mode); ignore */
        }
      }

      caption.addEventListener("click", toggle);
      caption.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          toggle();
        }
      });
    });
  });
})();
