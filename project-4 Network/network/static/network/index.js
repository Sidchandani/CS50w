// edit btn function
function edit(postid) {
    body=document.querySelector(`#post-body${postid}`).innerHTML;
    document.querySelector(`#edit-sec${postid}`).innerHTML=`<button type="button" class="btn btn-primary my-2" id="${postid}" onClick="save(this.id)">Save</button>
    <textarea id="save-body${postid}" cols="165" rows="3">${body}</textarea>`;
}

function save(postid) {
    var body=document.querySelector(`#save-body${postid}`).value;
    
    fetch(`/post/${postid}`, {
        method: 'PUT',
        body: JSON.stringify({
            body: body
        })
        })
        .then(response => response.json())
        .then(result => {
            document.querySelector(`#edit-sec${postid}`).innerHTML=`<button class="edit-btn p-0" id="${postid}" onClick="edit(this.id)">Edit</button>
            <h5 id="post-body${postid}">${body}</h5>`;
        });
}


function like(likeid,stat) {
    
    postid=parseInt(likeid.slice(4))
    usr=document.querySelector('#usrname').innerHTML;
    fetch(`/post/${postid}`, {
        method: 'PUT',
        body: JSON.stringify({
            like_status: stat,
            usr:usr
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            num=parseInt(document.querySelector(`#likes${postid}`).innerHTML);
            if (stat == 'like'){
                hrt='solid';
                num=num+1;
                now='unlike';
            }
            else{
                hrt='regular';
                num=num-1;
                now='like';
            }
            document.querySelector(`#${likeid}`).innerHTML=`<i class="fa-${hrt} fa-heart heart"></i>`;
            document.querySelector(`#likes${postid}`).innerHTML=num;
            document.querySelector(`#${likeid}`).value=now;
            console.log( document.querySelector(`#${likeid}`).value )
        });
}


function flw(status) {
    // get from layout.html
    follower=document.querySelector('#usrname').innerHTML;
    // get from user.html
    main=document.querySelector('#main-usr').innerHTML;
    
    fetch(`/follow/${status}`, {
        method: 'PUT',
        body: JSON.stringify({
            follower:follower,
            main: main
        })
      })
      .then(response => response.json())
      .then(result => {
        val=parseInt( document.querySelector('#followers').innerHTML);
        if (status == 'Follow'){
            now='Unfollow'
            val=val+1
        }
        else{
            val=val-1
            now='Follow'
        }
        document.querySelector('#followers').innerHTML=val;
        btn=document.querySelector(`#${status}`);
        btn.className=`btn ${now}`;
        btn.innerHTML=now;
        btn.id=now;



      });
    
}



document.addEventListener('DOMContentLoaded', function() {
    
    // console.log(document.querySelector('#usrname').innerHTML)
    // Select new post buttons
    try{
        document.querySelector('#new-post-btn').onclick = function() {

            body=document.querySelector('#new-post-body').value;
            // gets from layout.html
            username=document.querySelector('#usrname').innerHTML;
            if (body!=''){
                fetch('/post', {
                    method: 'POST',
                    body: JSON.stringify({
                        user:username,
                        body: body
                    })
                  })
                  .then(response => response.json())
                  .then(result => {
                      // Print result
                      console.log(result);
                      document.querySelector('#message').innerHTML='Successfully Posted 😊';
                      document.querySelector('#new-post-body').value='';
                    //   return window.location.reload();
                  });
            }
            else{document.querySelector('#message').innerHTML='Please provide some text..!!';}
        
        }

    }
    catch{
        // Do nothing
    }
    
})
