import { UserinfoService } from './../services/userinfo.service';
import { HttpClient } from '@angular/common/http';
import { Instance } from './../models/instance';
import { Component, OnInit, ComponentFactoryResolver, ViewContainerRef, ViewChild, ComponentRef, OnDestroy } from '@angular/core';
import { InstanceComponent } from '@app/home/instance/instance.component';
import { HomeDirective } from './home.directive';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  @ViewChild(HomeDirective, { static: true }) appHome: HomeDirective;
  componentRef: ComponentRef<InstanceComponent>;
  instances: Instance[];
  http: HttpClient;
  test: string;

  constructor(
    private userinfo: UserinfoService,
    private componentFactoryResolver: ComponentFactoryResolver
  ) {
    this.instances = [];
  }

  ngOnInit() {
    this.userinfo.getUserInfo()
      .subscribe(data => {
        data["instance"].forEach(element => {
          let temp: Instance;
          temp = {
            name: element["instance_name"],
            status: element["status"],
            ip: element["address"]["addr"]
          }
          this.createComponent(temp);
        });
      });

  }

  createComponent(instance: Instance) {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(InstanceComponent);
    const viewContainerRef = this.appHome.viewContainerRef;
    const componentRef = viewContainerRef.createComponent(componentFactory);
    componentRef.instance.instance = instance;
  }
}
