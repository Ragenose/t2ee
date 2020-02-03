import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[appHome]'
})
export class HomeDirective {

  constructor(public viewContainerRef: ViewContainerRef) { }

}
