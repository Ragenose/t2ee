import { VmService } from './../services/vm.service';
import { Instance } from './../models/instance';
import { Component, OnInit, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-instance',
  templateUrl: './instance.component.html',
  styleUrls: ['./instance.component.css']
})
export class InstanceComponent implements OnInit {
  @Input() instance: Instance;
  constructor(private vmService: VmService) { }

  ngOnInit() {
  }

  start(){
    this.vmService.startInstance(this.instance.name)
    .subscribe(
      data=>{
        alert("Successful Started");
        location.reload();
      },
      error=>console.log(error)
    )
  }

  shutdown(){
    this.vmService.shutoffInstance(this.instance.name)
    .subscribe(
      data=>{
        alert("Successful Shutdown");
        location.reload();
      },
      error=>console.log(error)
    )
  }

  reboot(){
    this.vmService.rebootInstance(this.instance.name)
    .subscribe(
      data=>{
        alert("Successful Rebooted");
        location.reload();
      },
      error=>console.log(error)
    )
  }

  delete(){
    this.vmService.deleteInstance(this.instance.name)
    .subscribe(
      data=>{
        alert("Successful Deleted");
        location.reload();
      },
      error=>console.log(error)
    )
  }
}
