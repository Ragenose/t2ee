import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

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
}
