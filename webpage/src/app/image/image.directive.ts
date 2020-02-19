import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[appImage]'
})
export class ImageDirective {

  constructor(public viewContainerRef: ViewContainerRef) { }

}
