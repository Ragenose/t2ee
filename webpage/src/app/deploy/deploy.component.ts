import { VmService } from './../services/vm.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-deploy',
  templateUrl: './deploy.component.html',
  styleUrls: ['./deploy.component.css']
})
export class DeployComponent implements OnInit {
  deployForm: FormGroup;
  images: string[];
  flavors: string[];

  constructor(private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private vmService: VmService) { }

  ngOnInit() {
    this.deployForm = this.formBuilder.group({
      image: ['', Validators.required],
      flavor: ['', Validators.required],
      instance_name: ['', Validators.required],
      root_password: ['', Validators.required]
    })
    this.images = ["Ubuntu16.04", "CentOS7"];
    this.flavors = ["small", "medium", "large"];
  }
  // convenience getter for easy access to form fields
  get f() { return this.deployForm.controls; }
  
  onDeploySubmit() {
    console.log(this.f.image.value);
    // stop here if form is invalid
    // if (this.deployForm.invalid) {
    //   return;
    // }
    this.vmService.deployInstance(
      this.f.instance_name.value,
      this.f.root_password.value,
      this.f.image.value,
      this.f.flavor.value
    ).subscribe(
      data=>{
        alert("Successful Deployed");
        this.router.navigate([""]);
      }
    )
    
  }
}
