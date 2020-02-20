import { Instance } from './models/instance';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BasicAuthInterceptor } from './helpers/basic-auth.interceptor';
import { ErrorInterceptor } from './helpers/error.interceptor';
import { HomeComponent } from './home/home.component';
import { InstanceComponent, DialogImageCreate } from './home/instance/instance.component';
import { HomeDirective } from './home/home.directive';
import { DeployComponent } from './deploy/deploy.component';
import { SettingComponent } from './setting/setting.component';
import { ImageComponent } from './image/image.component';
import { ImageDirective } from './image/image.directive';
import { ImageItemComponent, DialogImageDeploy } from './image/image-item/image-item.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    InstanceComponent,
    HomeDirective,
    DeployComponent,
    SettingComponent,
    DialogImageCreate,
    ImageComponent,
    ImageDirective,
    ImageItemComponent,
    DialogImageDeploy
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    ReactiveFormsModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: BasicAuthInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },

  ],
  bootstrap: [AppComponent],
  entryComponents: [ HomeComponent, InstanceComponent, DialogImageCreate, ImageComponent, ImageItemComponent, DialogImageDeploy ]
})
export class AppModule { }
