import { SettingComponent } from './setting/setting.component';
import { DeployComponent } from './deploy/deploy.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { AuthGuard } from './helpers/auth.guard';
import { HomeComponent } from './home/home.component';
import { ImageComponent } from './image/image.component';

const routes: Routes = [
  {path: '', component: HomeComponent, canActivate: [AuthGuard]},
  {path: 'deploy', component: DeployComponent, canActivate: [AuthGuard]},
  {path: 'login', component: LoginComponent},
  {path: 'setting', component: SettingComponent},
  {path: 'image', component: ImageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
