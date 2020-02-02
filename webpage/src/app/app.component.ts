import { AuthenticationService } from './services/authentication.service';
import { Component } from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';
import { MatIconRegistry } from '@angular/material/icon';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(
    iconRegistry: MatIconRegistry, 
    sanitizer: DomSanitizer,
    private authenticationService: AuthenticationService,
    private router: Router) {
    iconRegistry.addSvgIcon(
        'account',
        sanitizer.bypassSecurityTrustResourceUrl('assets/img/account_circle-24px.svg'));
  }

  logout(){
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
}
