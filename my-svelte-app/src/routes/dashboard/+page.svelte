<script lang="ts">
    import { marked } from "marked";
    import { writable } from "svelte/store";
    import{user_num} from "$lib/store"

// let markdown = `
// # 标题                                                                                                  
// 这是**粗体**和*斜体*

// - 列表1
// - 列表2
// \`\`\`javascript                                                                                                        
// console.log('hello');                                                                                                   
// \`\`\`                                                                                                                  
// `; 
//     let html=marked.parse(markdown)
//     let tokens=marked.lexer(markdown)
    const num=writable(10);
    // num.subscribe(
    //     (value)=>{
    //         console.log("当前值",value)
    //     }
    // )
    $: console.log("当前值",$num)
    function click(){
        num.update(n=>n+1)
    }
    function show_user_num(){
        $user_num++;
        console.log($user_num)
    }
   
</script>                                                                                                        

<!-- <div class="markdown-body">{@html html}</div> -->
<button on:click={show_user_num}>test</button>

<style>                                                                                                               
    /* 加 :global() 让样式作用于 @html 内容 */                                                                            
    .markdown-body h1 {                                                                                          
        color: purple;                                                                                                    
        font-size: 2em;                                                                                                   
    }                                                                                                                     
                                                                                                                          
    .markdown-body ul {                                                                                          
        list-style: disc;                                                                                                 
        padding-left: 20px;                                                                                               
    }                                                                                                                     
                                                                                                                          
    .markdown-body pre{                                                                                         
        background: #1e1e1e;                                                                                              
        color: #fff;                                                                                                      
        padding: 10px;                                                                                                    
        border-radius: 5px;                                                                                               
    }                                                                                                                     
                                                                                                                          
    .markdown-body code {                                                                                        
        background: #f0f0f0;                                                                                              
        padding: 2px 5px;                                                                                                 
        border-radius: 3px;                                                                                               
    }                                                                                                                     
    </style>            
