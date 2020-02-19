import { ImageItemComponent } from './image-item/image-item.component';
import { ImageDirective } from './image.directive';
import { ImageService } from './../services/image.service';
import { Component, OnInit, ComponentFactoryResolver, ViewChild, ComponentRef } from '@angular/core';
import { UserinfoService } from '@app/services/userinfo.service';

export interface Image{
  name: string,
  description: string,
  username: string,
  baseImage: string
}

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent implements OnInit {
  @ViewChild(ImageDirective, { static: true }) appImage: ImageDirective;
  componentRef: ComponentRef<ImageItemComponent>;

  constructor(
    private imageList: ImageService,
    private componentFactoryResolver: ComponentFactoryResolver
  ) { }

  ngOnInit() {
    this.imageList.getImageList()
    .subscribe((data: string[])=>{
      data.forEach(element => {
        let temp: Image;
        temp = {
          name: element["image_name"],
          description: element["description"],
          username: element["username"],
          baseImage: element["base_image_name"]
        }
        this.createComponent(temp);
      });
    });
  }

  createComponent(image: Image) {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(ImageItemComponent);
    const viewContainerRef = this.appImage.viewContainerRef;
    const componentRef = viewContainerRef.createComponent(componentFactory);
    componentRef.instance.image = image;
  }
}
