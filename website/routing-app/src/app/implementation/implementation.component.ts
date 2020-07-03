import { Component, OnInit, HostListener } from '@angular/core';

@Component({
  selector: 'app-implementation',
  templateUrl: './implementation.component.html',
  styleUrls: ['./implementation.component.css']
})
export class ImplementationComponent implements OnInit {

  constructor() { }
  mybutton = null;
  ngOnInit(): void {
    this.mybutton = document.getElementById("myBtn");
    console.log("my button is: " + this.mybutton);
  }

  scrollFunction(): void {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      this.mybutton.style.display = "block";
    } else {
      this.mybutton.style.display = "none";
    }
  }
  topFunction(): void {
    console.log('executed');
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }
  @HostListener("window:scroll", []) onWindowScroll() {
    // do some stuff here when the window is scrolled
    this.scrollFunction();
  }

}
