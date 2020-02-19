import { Image } from './../image.component';
import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-image-item',
  templateUrl: './image-item.component.html',
  styleUrls: ['./image-item.component.css']
})
export class ImageItemComponent implements OnInit {
  @Input() image: Image;

  constructor() { }

  ngOnInit() {
  }

}
