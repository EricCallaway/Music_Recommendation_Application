class SideNavbar extends HTMLElement{
    constructor(){
        super();
    }

    connectedCallback(){
        this.innerHTML = `<div class="wrapper">
        <!--Top menu-->
        <div class="sidebar">
            <!--Profile Image & text-->
            <div class="logo">
                <img src="../imgs/music_clip_art.png" alt="music_logo">
                <h3>Eric Callaway's</h3>
                <p>Music Recommendation Application</p>
            </div>
            <!--Menu item-->
            <div class="menu-container">
                <ul>
                    <li>
                        <a href="#" class="active">
                            <span class="icon"><i class="fa-solid fa-house"></i></span>
                            <span class="item">Home</span>
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <span class="icon"><i class="fa-sharp fa-solid fa-screwdriver-wrench"></i></span>
                            <span class="item">Admin</span>
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <span class="icon"><i class="fa-solid fa-code-branch"></i></span>
                            <span class="item">Model</span>
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <span class="icon"><i class="fa-solid fa-music"></i></span>
                            <span class="item">Recommendations</span>
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <span class="icon"><i class="fas fa-users"></i></span>
                            <span class="item">Users</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>`
    }
}

customElements.define('side-navbar', SideNavbar)