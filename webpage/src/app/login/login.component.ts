import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AuthenticationService } from '@app/services/authentication.service';

@Component({ 
  selector: 'app-nav',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'] })
export class LoginComponent implements OnInit {
    loginForm: FormGroup;
    signupForm: FormGroup;
    loading = false;
    submittedLogin = false;
    submittedSignup = false;
    returnUrl: string;
    errorLogin = '';
    errorSignup= '';

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService
    ) { 
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) { 
            this.router.navigate(['/']);
        }
    }

    ngOnInit() {
        this.loginForm = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required]
        });
        
        this.signupForm = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required],
            email: ['', Validators.required]
        });
        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    // convenience getter for easy access to form fields
    get f() { return this.loginForm.controls; }
    get s() {return this.signupForm.controls;}

    onLoginSubmit() {
        this.submittedLogin = true;

        // stop here if form is invalid
        if (this.loginForm.invalid) {
            return;
        }

        this.loading = true;
        this.authenticationService.login(this.f.username.value, this.f.password.value)
            .pipe(first())
            .subscribe(
                data => {
                    this.router.navigate([this.returnUrl]);
                },
                error => {
                    this.errorLogin = error;
                    this.loading = false;
                });
    }

    onSignupSubmit(){
        this.submittedSignup = true;

        // stop here if form is invalid
        if (this.signupForm.invalid) {
            return;
        }

        this.loading = true;
        this.authenticationService.signup(this.s.username.value, this.s.password.value, this.s.email.value)
            .pipe(first())
            .subscribe(
                data => {
                    this.router.navigate([this.returnUrl]);
                },
                error => {
                    this.errorLogin = error;
                    this.loading = false;
                });
    }
}