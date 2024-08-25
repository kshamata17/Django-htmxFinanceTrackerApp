document.getElementById('toggleSidebar').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    var content = document.getElementById('content');
    
    sidebar.classList.toggle('expanded');
    content.classList.toggle('expanded');
});