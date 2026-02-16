<script>
    let{children}=$props();
</script>
<nav style="background: #ff0000; color: white; padding: 10px;"></nav>

<div style="display: flex;">                                                                            
    <aside style="width: 200px; background: #eee; padding: 10px;">                                      
        侧边栏                                                                                          
    </aside>                                                                                            
    <main style="flex: 1; padding: 10px;">                                                              
        {@render children()}                                                                            
    </main>                                                                                             
</div>