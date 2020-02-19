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
  MatSelectModule,
  MatDialogModule
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
    TextFieldModule,
    MatDialogModule
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
    TextFieldModule,
    MatDialogModule
  ]
})
export class MaterialModule { }