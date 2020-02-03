import { Instance } from './../models/instance';
import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-instance',
  templateUrl: './instance.component.html',
  styleUrls: ['./instance.component.css']
})
export class InstanceComponent implements OnInit {
  @Input() instance: Instance;
  constructor() { }

  ngOnInit() {
  }

}
