

ScrollRate = 25;

    function scrollDiv_init() {
      DivElmnt = document.getElementById('scrollingDiv');
      ReachedMaxScroll = false;
      
      DivElmnt.scrollTop = 0;
      PreviousScrollTop  = 0;
      
      ScrollInterval = setInterval('scrollDiv()', ScrollRate=25);
    }
    
    function scrollDiv() { 
      if (!ReachedMaxScroll) {
        DivElmnt.scrollTop = PreviousScrollTop;
        PreviousScrollTop++;
        
        ReachedMaxScroll = DivElmnt.scrollTop >= (DivElmnt.scrollHeight - DivElmnt.offsetHeight);
      }
      else {
        DivElmnt.scrollTop = PreviousScrollTop = 0;
        ReachedMaxScroll = false;
      }
    }
    
    function pauseDiv() {
      clearInterval(ScrollInterval);
    }
    
    function resumeDiv() {
      PreviousScrollTop = DivElmnt.scrollTop;
      ScrollInterval    = setInterval('scrollDiv()', ScrollRate=25);
    }
  