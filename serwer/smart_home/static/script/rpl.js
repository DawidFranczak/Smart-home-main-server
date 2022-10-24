async function select_rpl(e){
    switch (e.target.id){
      case 'lamp':
        console.log(e.target.id)
        const dict = {'action':'get',
                      'id':e.target.value}
        data = await sendData('POST',dict)
      
        console.log(data)
        document.querySelectorAll('#rfid').forEach(r =>{
          r.checked = false;
          for(id of data['rfid']){
            if(r.value == id) {
              r.checked = true; 
              break;
            }
          }
      
        })
        document.querySelectorAll('#btn').forEach(r =>{
          r.checked = false;
          console.log(data)
          for(id of data['btn']){
            if(r.value == id) {
              r.checked = true; 
              break;
            } 
          }    
        })
        break;
      case 'rpl-btn':
        rpl_connect()
        break;
    }
  }
  
  async function rpl_connect(){
    let lamp = document.querySelectorAll('#lamp');
    let rfid = document.querySelectorAll('#rfid');
    let btn = document.querySelectorAll('#btn');
    let rfids = [];
    let btns = [];
    let lampID
    lamp.forEach(lamp => {
      if(lamp.checked){
        lampID = lamp.value; 
      }
    })
    rfid.forEach(rfid => {
      if(rfid.checked){
        rfids.push(rfid.value);
      }
    })
    btn.forEach(btn => {
      if(btn.checked){ 
        btns.push(btn.value);
      }
    })
    dict = {
        'action': 'connect',
        'lamp': lampID,
        'rfids':rfids,
        'btns':btns
    }
  
    sendData('POST',dict)
  }

  window.onload = function(){
    document.querySelector('.rpl-containers').addEventListener('click',select_rpl);  
  }