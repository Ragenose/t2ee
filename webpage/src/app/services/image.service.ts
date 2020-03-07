import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  constructor(private http: HttpClient) { }

  getImageList(){
    return this.http.get("/api/image/list");
  }

  deleteImage(image_name: string){
    return this.http.delete("/api/image/delete/"+image_name)
  }
}
