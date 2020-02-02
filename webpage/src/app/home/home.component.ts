import { UserinfoService } from './../services/userinfo.service';
import { HttpClient } from '@angular/common/http';
import { Instance } from './../models/instance';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  instances: Instance[];
  http: HttpClient;
  test: string;

  constructor(
    private userinfo: UserinfoService
  ) { }

  ngOnInit() {
    this.userinfo.getUserInfo()
    .subscribe(data =>{
      data["instance"].forEach(element => {
        let temp: Instance;
        temp = {
          name : element["instance_name"],
          status : element["status"],
          ip : element["address"]["addr"]
        }
      });
      
    });

  }

}
