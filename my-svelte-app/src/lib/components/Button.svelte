<script>                                                                                                
    let props=$props() ;
    console.log('收到的参数',props);          
    let {                                                                                                   
      text = '按钮',                                                                                      
      type = 'primary',                                                                                   
      disabled = false,                                                                                   
      onclick = () => {}                                                                                  
  } = props;      
    // export let test=""
  
</script>

<button                                                                                                 
class="btn btn-{type}"                                                                              
{disabled}                                                                                          
onclick={onclick}                                                                                   
>                                                                                                       
{text}                                                                                              
</button> 

<style>                                                                                                 
    .btn {                                                                                                  
        padding: 10px 20px;                                                                                 
        border: none;                                                                                       
        border-radius: 6px;                                                                                 
        cursor: pointer;                                                                                    
    }                                                                                                       
    .btn-primary { background: #3b82f6; color: white; }                                                     
    .btn-danger { background: #ef4444; color: white; }                                                      
    </style> 