# Exercise 8 - Capstone Challenge: ApproveThis Requires Approvals!

**Duration**: 60+ minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Apply all techniques learned throughout the workshop
- Implement a complete feature from planning to deployment autonomously
- Work with Copilot as a development partner for complex requirements
- Demonstrate mastery of SDLC integration with AI assistance
- Make architectural decisions with AI guidance
- Deliver a production-ready feature end-to-end

## 📸 Scenario: The Signature Feature of ApproveThis

🏢 Your manager at ShipIt Industries calls you into her office with exciting news:

> "The team loves what you've built so far! But here's the irony: we have an application called **ApproveThis** that doesn't actually have approval workflows yet! 
>
> Management has been asking when we can start using the approval feature. They want all production workflow dispatches to require approval from a GlobalAdmin before they execute. This is critical for our compliance and security policies.
>
> I know this is a complex feature, but you've proven yourself throughout this project. I'm confident you can implement this with Copilot's help. You have the rest of the sprint to get it done. Show me what you can do!"

This is your chance to shine! You'll implement the complete approval workflow feature that gives ApproveThis its name. And the best part? You have GitHub Copilot as your partner throughout the entire process.

---

## The Challenge: Implement Approval Workflows

### High-Level Requirements

ApproveThis needs a complete approval workflow system with these capabilities:

**For Users with DISPATCH_WORKFLOW Permission (LeadDeveloper role):**
- Request workflow dispatch (creates a "pending approval" dispatch request)
- View status of their approval requests
- Receive notification when requests are approved/rejected
- Cancel pending requests

**For Users with MANAGE_APPROVALS Permission (GlobalAdmin role):**
- View all pending approval requests
- Approve requests (which triggers the workflow dispatch)
- Reject requests with a reason
- View approval history

**System Requirements:**
- All workflow dispatches **must** go through approval (no direct dispatch)
- Approval status tracked in DispatchRequest model
- Audit trail: who approved/rejected, when, and why
- Approved dispatches automatically trigger the workflow
- Proper RBAC enforcement throughout

---

## Step 1: Planning with Copilot and Azure DevOps MCP

Start by using the planning techniques from Lab 3.

### 1.1 Create Work Items for the Feature

<details>
<summary>💡 Example prompt</summary>

```
@workspace @azure-devops Based on the approval workflow requirements, help me create a comprehensive set of user stories in Azure DevOps. Consider:
- User stories for requesting approval
- User stories for approving/rejecting
- Technical tasks for model updates
- Technical tasks for route implementation
- Technical tasks for UI development
- Testing tasks
- Documentation tasks
Group them logically and identify dependencies.
```

</details>

### 1.2 Create Technical Design Document

Use Copilot to draft the technical approach:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a technical design document for the approval workflow feature. Include:
1. Database schema changes (if any needed)
2. New API endpoints required
3. UI screens and flows
4. Sequence diagrams for approval process
5. Security considerations
6. Testing strategy
Save as docs/Approval-Workflow-Design.md
```

</details>

### 1.3 Review Existing Models

Examine the DispatchRequest model to see what's already available:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Review app/models/dispatch_request.py. Does it already have fields for approvals (approved_by, approved_at, rejection_reason, etc.)? What fields might we need to add?
```

</details>

> [!TIP]
> 💡 The DispatchRequest model likely already has approval-related fields from the original design! This is a key discovery that will save implementation time.

---

## Step 2: Implementing the Database Layer

### 2.1 Update the DispatchRequest Model (if needed)

If the model needs additional fields:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Update app/models/dispatch_request.py to support the approval workflow. Ensure it has:
- approved_at (timestamp)
- approved_by_id (foreign key to User)
- rejection_reason (text)
- status (pending/approved/rejected/completed/failed)
Add any other fields necessary for complete audit trail.
```

</details>

### 2.2 Create Database Migration

Generate a migration for your changes:

```bash
cd approvethis
flask db migrate -m "Add approval workflow fields to DispatchRequest"
flask db upgrade
```

If you need help with the migration:

<details>
<summary>💡 Example prompt</summary>

```
@workspace The migration in migrations/versions/[latest].py needs to be reviewed. Verify it correctly adds/modifies the approval fields for DispatchRequest.
```

</details>

### 2.3 Add Model Methods for Approval Logic

Add helper methods to the model:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Add methods to the DispatchRequest model in app/models/dispatch_request.py:
- approve(user) - Mark as approved by given user
- reject(user, reason) - Mark as rejected with reason
- can_be_approved_by(user) - Check if user has permission to approve
- is_pending() - Check if request is pending approval
Include proper validation and timestamp updates.
```

</details>

---

## Step 3: Implementing API Endpoints

Create the backend API for approval operations.

### 3.1 Create Approval Routes

<details>
<summary>💡 Example prompt</summary>

```
@workspace Implement API routes for approval workflow in app/blueprints/api/routes.py or create a new approvals blueprint. Include:

POST /api/approvals/requests - Create new dispatch request (pending approval)
GET /api/approvals/pending - List all pending approvals (admin only)
GET /api/approvals/my-requests - List current user's requests
POST /api/approvals/<id>/approve - Approve a request (admin only)
POST /api/approvals/<id>/reject - Reject a request with reason (admin only)
DELETE /api/approvals/<id> - Cancel own pending request

Include:
- Proper RBAC checks using @permission_required decorator
- Input validation
- Error handling
- Success/error responses in JSON
- Logging of approval actions
```

</details>

### 3.2 Implement Dispatch Trigger on Approval

When a request is approved, it should trigger the workflow:

<details>
<summary>💡 Example prompt</summary>

```
@workspace When a dispatch request is approved, we need to:
1. Update the dispatch request status to 'approved'
2. Trigger the actual workflow dispatch via the GitHub provider
3. Update status to 'completed' or 'failed' based on result
4. Log the action for audit trail

Implement this logic in the approve endpoint. Use the existing GitHub provider pattern from app/providers/.
```

</details>

### 3.3 Add Notification Hooks (Optional Enhancement)

For extra credit, add notifications:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Add notification hooks for approval events:
- When request is created (notify admins)
- When request is approved (notify requester)
- When request is rejected (notify requester with reason)

Use a simple notification system (email, webhook, or in-app notifications).
```

</details>

---

## Step 4: Building the User Interface

Create the UI components for the approval workflow.

### 4.1 Create Approval Request Form

Build the form for requesting dispatch with approval:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a UI form for requesting workflow dispatch with approval in app/templates/. The form should:
- Show workflow details (name, repository, branch)
- Allow input of workflow parameters
- Clearly indicate this will create an approval request (not immediate dispatch)
- Submit to the new API endpoint
- Follow the existing template patterns and styling
Save as app/templates/workflows/request_dispatch.html
```

</details>

### 4.2 Create Pending Approvals Dashboard

For GlobalAdmin users:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a pending approvals dashboard for GlobalAdmin users. Display:
- List of all pending dispatch requests
- Request details: user, workflow, repository, timestamp
- Approve and Reject buttons
- Modal for entering rejection reason
- Real-time status updates (optional: use AJAX/fetch)
Follow existing template conventions and styling.
Save as app/templates/approvals/pending.html
```

</details>

### 4.3 Create My Requests Page

For users to track their own requests:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a "My Dispatch Requests" page showing:
- All requests by current user
- Status (pending, approved, rejected, completed, failed)
- Timestamp of request and approval/rejection
- For rejected: show rejection reason
- For pending: option to cancel
- For approved/completed: link to workflow run
Save as app/templates/approvals/my_requests.html
```

</details>

### 4.4 Update Navigation

Add links to the new pages in the navigation:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Update app/templates/base.html or navigation template to add:
- "Request Dispatch" option in workflows dropdown (for LeadDeveloper+)
- "Pending Approvals" in main nav (for GlobalAdmin only)
- "My Requests" in user dropdown (for LeadDeveloper+)
Use proper RBAC checks to show/hide based on permissions.
```

</details>

---

## Step 5: Testing the Feature

Comprehensive testing is critical for a feature this important!

### 5.1 Unit Tests for Model Logic

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create unit tests for the approval methods in DispatchRequest model:
- test_approve_request
- test_reject_request  
- test_can_be_approved_by_with_permission
- test_can_be_approved_by_without_permission
- test_cannot_approve_own_request
- test_status_transitions
Save as tests/test_models/test_dispatch_request_approval.py
```

</details>

### 5.2 API Endpoint Tests

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create API tests for approval endpoints:
- Test creating dispatch request creates pending approval
- Test admin can approve pending request
- Test admin can reject with reason
- Test non-admin cannot approve
- Test user can view their own requests
- Test user cannot approve their own request
- Test approved request triggers workflow dispatch
Use pytest fixtures from conftest.py for authenticated clients.
Save as tests/test_routes/test_approvals.py
```

</details>

### 5.3 End-to-End Tests with Playwright

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create E2E Playwright tests for the complete approval workflow:
1. Developer logs in and requests workflow dispatch
2. Request appears as pending in developer's "My Requests"
3. Developer logs out, GlobalAdmin logs in
4. Admin sees request in "Pending Approvals"
5. Admin approves the request
6. Developer logs back in and sees "Approved" status
7. Workflow is dispatched (verify via API or mock)

Also create rejection flow test:
1. Developer requests dispatch
2. Admin rejects with reason "Invalid parameters"
3. Developer sees rejected status with reason

Save as tests/e2e/test_approval_workflow.py
```

</details>

### 5.4 Run All Tests

Execute the complete test suite:

```bash
cd approvethis
pytest tests/ -v --cov=app --cov-report=html
```

Ensure you meet the 80% coverage requirement!

---

## Step 6: Code Review and Security

Before deployment, perform thorough review.

### 6.1 Copilot Code Review

<details>
<summary>💡 Example prompt</summary>

```
@workspace Perform a comprehensive code review of the approval workflow implementation. Focus on:
- Security: Can users approve their own requests? Can non-admins approve?
- RBAC: Are all endpoints properly protected?
- SQL Injection: Is user input validated?
- XSS: Are outputs properly escaped in templates?
- Authorization bypass: Are there ways to circumvent approval?
- Audit trail: Is every action logged?
```

</details>

### 6.2 Test Permission Boundaries

Explicitly test security boundaries:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create security tests that attempt to bypass approvals:
- Viewer trying to approve requests
- Developer approving their own request
- Direct API calls without authentication
- Manipulating request IDs to approve others' requests
- SQL injection in rejection reason field
These should all fail! Save as tests/test_security_approvals.py
```

</details>

---

## Step 7: Documentation

Document the feature for users and developers.

### 7.1 User Guide

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a user guide for the approval workflow feature:
- How to request a workflow dispatch
- How to track request status
- How to cancel a pending request
- (For admins) How to review and approve/reject requests
- Screenshots or ASCII diagrams of the workflow
Save as docs/Approval-Workflow-User-Guide.md
```

</details>

### 7.2 API Documentation

<details>
<summary>💡 Example prompt</summary>

```
@workspace Generate API documentation for the approval endpoints in OpenAPI/Swagger format. Include:
- Endpoint paths and methods
- Request/response schemas
- Authentication requirements
- Permission requirements
- Example requests and responses
Save as docs/api/approvals-api.yaml
```

</details>

### 7.3 Update Main README

<details>
<summary>💡 Example prompt</summary>

```
@workspace Update the main README.md in approvethis/ to include:
- Overview of the approval workflow feature
- Link to user guide
- Link to API documentation
- Note about MANAGE_APPROVALS permission requirement
```

</details>

---

## Step 8: Deployment

Deploy your feature to the dev environment.

### 8.1 Create Database Migration in Dev

Ensure migrations are applied:

```bash
# In dev environment
flask db upgrade
```

### 8.2 Deploy via GitHub Actions

Trigger deployment workflow:

1. Commit all changes
2. Push to feature branch
3. Create pull request
4. Deploy to dev environment via GitHub Actions
5. Verify deployment successful

### 8.3 Manual Verification in Dev

Test the deployed feature:

- [ ] Login as developer, request a dispatch
- [ ] Login as admin, see pending request
- [ ] Approve the request
- [ ] Verify workflow was triggered
- [ ] Test rejection flow
- [ ] Verify audit logs

---

## 🏆 Challenge Complete!

If you've reached this point, congratulations! You've implemented a production-ready feature using AI assistance throughout the entire SDLC.

### ✅ Success Criteria

Verify you've met all requirements:

- [ ] Dispatch requests can be created with "pending approval" status
- [ ] GlobalAdmin can view pending approvals
- [ ] Approvals and rejections are tracked with user and timestamp
- [ ] Rejected dispatches show rejection reason
- [ ] Approved dispatches trigger the workflow automatically
- [ ] Users cannot approve their own requests
- [ ] Viewers cannot approve any requests
- [ ] Tests pass for all new functionality (unit, integration, E2E)
- [ ] Test coverage is at least 80% for new code
- [ ] Security review shows no critical vulnerabilities
- [ ] Documentation is complete (user guide, API docs)
- [ ] Feature deployed and verified in dev environment

---

## 🤔 Reflection Questions

Take a moment to reflect on your journey:

1. How did your approach to this feature differ from how you would have built it without Copilot?
2. What aspects of the implementation did Copilot handle particularly well?
3. Where did you need to exercise human judgment over AI suggestions?
4. How confident are you in deploying this to production? What additional steps would you take?
5. How has this workshop changed your perspective on AI in the SDLC?

---

## 🎓 Key Takeaways from the Workshop

Reflecting on the entire workshop journey:

### Planning (Lab 3)
- **MCP integration** brings external context (Azure DevOps, infrastructure) into Copilot
- **Governance policies** can be encoded in `.github/copilot-instructions.md`
- **Work item integration** keeps planning and coding connected

### Development (Lab 4)
- **Agent mode** for complex, multi-file features
- **Edit mode** for surgical, targeted changes
- **Multitasking** enabled by separate conversation contexts
- **Code review** catches issues before they reach production

### Testing (Lab 5)
- **AI test generation** achieves high coverage quickly
- **Edge case discovery** with Copilot suggestions
- **E2E tests** validate complete user workflows
- **Testing is integrated**, not an afterthought

### Infrastructure (Lab 6)
- **Infrastructure MCP** enables AI-assisted IaC
- **Terraform validation** prevents costly mistakes
- **Job execution framework** integrates operations into application

### Capstone (Lab 8)
- **End-to-end feature delivery** with AI partnership
- **Autonomous work** with Copilot as a development partner
- **Production-ready code** with proper testing and security
- **Complete SDLC integration** from planning to deployment

---

## 🎉 Congratulations!

You've completed the GitHub Copilot Advanced Workshop: SDLC Integration! 

You've learned to:
- ✅ Use GitHub Copilot throughout the entire software development lifecycle
- ✅ Integrate external systems via Model Context Protocol (MCP)
- ✅ Implement features using advanced Copilot modes (Edit, Agent)
- ✅ Generate comprehensive test suites with AI assistance
- ✅ Manage infrastructure as code with Copilot and MCP
- ✅ Deliver production-ready features autonomously with AI partnership

### What's Next?

**Apply these skills in your work:**
- Set up MCP servers for your organization's tools
- Create `.github/copilot-instructions.md` for your projects
- Use Agent mode for complex features, Edit mode for focused changes
- Generate tests as you code, not after
- Let Copilot help with infrastructure and documentation

**Continue Learning:**
- Explore additional MCP servers for your tech stack
- Configure custom Copilot agents for specialized tasks
- Share best practices with your team
- Contribute to the Copilot community

---

## 🏢 Thank You from ShipIt Industries!

The ApproveThis application is now ready to help ShipIt Industries manage their CI/CD processes safely and efficiently. Thanks to your work, they can now:
- View all jobs and deployments in one place
- Control workflows across multiple platforms
- Require approvals before critical deployments
- Use RBAC for safe, team-wide access

Most importantly, they now have **ApproveThis with approvals**! 🚀

---

**[← Back to Lab 7](Lab-7-CI-CD-Beyond-GitHub-Actions.md)**
