import { SettingService } from './../services/setting.service';
import { AuthenticationService } from './../services/authentication.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-setting',
  templateUrl: './setting.component.html',
  styleUrls: ['./setting.component.css']
})
export class SettingComponent implements OnInit {
  pubkeyForm: FormGroup;
  passwordForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
    private settingService: SettingService
  ) { }

  get pubkeyFormControl(){
    return this.pubkeyForm.controls;
  }

  ngOnInit() {
    this.pubkeyForm = this.formBuilder.group({
      pubkey: ['', Validators.required]
    })
  }

  onPubkeySubmit(){
    if(this.pubkeyForm.invalid){
      return;
    }

    this.settingService.updatePubkey(this.pubkeyFormControl.pubkey.value)
    .subscribe(
      data=>{
        alert("Successful Updated");
      }
    )
    
  }
}
