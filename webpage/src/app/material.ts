import { NgModule } from '@angular/core';

import {
  MatToolbarModule,
  MatButtonModule,
  MatSidenavModule,
  MatIconModule,
  MatListModule,
  MatStepperModule,
  MatInputModule,
  MatFormFieldModule,
  MatTabsModule,
  MatCardModule,
  MatMenuModule,
  MatSelectModule 
} from '@angular/material';

import {
  TextFieldModule
} from '@angular/cdk/text-field';

@NgModule({
  imports: [
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatStepperModule,
    MatInputModule,
    MatFormFieldModule,
    MatTabsModule,
    MatCardModule,
    MatMenuModule,
    MatSelectModule,
    TextFieldModule
  ],
  exports: [
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatStepperModule,
    MatInputModule,
    MatFormFieldModule,
    MatTabsModule,
    MatCardModule,
    MatMenuModule,
    MatSelectModule,
    TextFieldModule
  ]
})
export class MaterialModule { }