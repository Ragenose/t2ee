import { Instance } from './../models/instance';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class VmService {

  constructor(private http: HttpClient) { }

  deleteInstance(name: string){
    return this.http.delete('/api/instance/delete/'+name);
  }

  startInstance(name: string){
    return this.http.post('/api/instance/lifecycle/start/'+name, "");
  }

  shutoffInstance(name: string){
    return this.http.post('/api/instance/lifecycle/shutdown/'+name, "");
  }

  rebootInstance(name: string){
    return this.http.post('/api/instance/lifecycle/reboot/'+name, "");
  }

  deployInstance(instance_name: string, root_password: string, image: string, flavor: string){
    let httpHeaders = new HttpHeaders;
    httpHeaders = httpHeaders.append("Content-Type", "application/json");
    return this.http.post("/api/instance/create",{
      "instance_name": instance_name,
      "flavor": flavor,
      "image": image,
      "root_password": root_password
    }, {headers: httpHeaders});
  }

  createImage(instance_name: string, image_name: string, description: string){
    let httpHeaders = new HttpHeaders;
    httpHeaders = httpHeaders.append("Content-Type", "application/json");
    return this.http.post("/api/image/create",{
      "instance_name": instance_name,
      "image_name": image_name,
      "description": description
    }, {headers: httpHeaders});
  }

  transfer(instance_name: string, new_owner: string){
    let httpHeaders = new HttpHeaders;
    httpHeaders = httpHeaders.append("Content-Type", "application/json");
    return this.http.post("/api/instance/transfer",{
      "instance_name": instance_name,
      "new_owner": new_owner
    }, {headers: httpHeaders});
  }
}


