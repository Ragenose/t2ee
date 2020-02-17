import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Md5 } from 'ts-md5';

@Injectable({
  providedIn: 'root'
})
export class SettingService {

  constructor(private http: HttpClient) { }

  updatePubkey(key: string){
    return this.http.post('/api/user/keypair/update',
    {
      "pubkey": key
    })
  }

  updatePassword(password: string){
    let hashedPassword = Md5.hashStr(password);
    return this.http.post('/api/user/update/password',
    {
      "password": hashedPassword
    })
  }
}
