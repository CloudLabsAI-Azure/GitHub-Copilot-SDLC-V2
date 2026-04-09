# Exercise 8 - Capstone Challenge: ApproveThis Requires Approvals!

**Duration**: 60 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Apply all techniques learned throughout the workshop
- Implement a complete feature from planning to deployment autonomously
- Work with Copilot as a development partner for complex requirements
- Demonstrate mastery of SDLC integration with AI assistance
- Make architectural decisions with AI guidance
- Deliver a production-ready feature end-to-end

## 🏢 The Approval Challenge at ShipIt Industries

Erica messages you and asks if you can stop by her desk for a moment.

> **Erica**: "You've done excellent work on ApproveThis. The GitHub integration is solid, tests are comprehensive, infrastructure is deployed, and things are running pretty smoothly.
>
> Now it's time to implement the feature I'm sure you've been expecting: **actual workflow approvals**! The app is named ApproveThis for a reason, after all.
>
> Here's the sitch: Right now, any LeadDeveloper can dispatch any workflow. But some workflows are critical - production deployments, database migrations, security updates. We need an approval system. There's mainly 2 different scenarios we need to support:
> 
> Workflows triggered by users via the ApproveThis UI
> - Certain workflows require approval before they run
> - Developers can request dispatches, but they go into 'pending approval' state
> - Approvers (GlobalAdmins or designated approvers) can review and approve/reject
> - Once approved, the workflow actually dispatches
> - Full audit trail of who requested, who approved, when, and why
>
> Workflows triggered via GitHub Actions
> - Some workflows are triggered automatically via GitHub Actions (e.g., on push to main)
> - GitHub environments can require approvals before proceeding with allowing workflow jobs to run
> - The action creates a pending dispatch request in ApproveThis
> - Approvers review and approve/reject in ApproveThis
> - Once approved, the GitHub Action job continues
> - Full audit trail as above

> I'm giving you full autonomy on this. You've learned all the tools - planning with MCP, development with Agent mode, testing, deployment. Put it all together. Show me what you can do.
>
> Oh and no pressure but can you have this done by the end of the day? 😅"

With that, Erica returns to her work and you head back to your desk. It's time to get cracking on these approval workflows!

> **This lab is intentionally less prescriptive.** You'll make decisions, choose approaches, and solve problems independently. Use Copilot as your assistant, but you're the developer in charge.
>
> After reading through the high-level requirements, plan your approach. Break the work into manageable pieces. Implement, iterate, and deploy the feature end-to-end.
>
> **Focus on delivering a minimum viable product.** Don't worry about making it perfect. This lab intentionally gives you more work than you can reasonably complete in an hour. The goal is to practice prioritization and decision-making with Copilot as your partner.

---

## The Challenge: Implement Approval Workflows

### High-Level Requirements

ApproveThis needs a complete approval workflow system with these capabilities:

**For Users with DISPATCH_WORKFLOW Permission (LeadDeveloper role):**
- Request workflow dispatch
    - Creates a "pending approval" dispatch request
    - Use existing Azure function to trigger dispatch after approval
- View status of their approval requests
- Receive notification when requests are approved/rejected
    - For the purposes of this lab, notifications can be simple console logs or in-app messages
- Cancel pending requests
    - Should not be able to cancel other users' requests

**For Users with MANAGE_APPROVALS Permission (GlobalAdmin role):**
- View all pending approval requests
- Approve requests (which triggers the workflow dispatch)
- Reject requests with a reason
- View approval history

**System Requirements:**
- Workflow dispatches **must** go through approval if touching production systems
    - For this lab, assume any workflow configured with a "production" environment requires approval
- Approval status tracked in DispatchRequest model
- Audit trail: who approved/rejected, when, and why
- Approved dispatches automatically trigger the workflow
- Proper RBAC enforcement throughout

## 🧐 Tips & Recommendations

This section provides tips and suggestions to help you succeed. How you approach the implementation is up to you!

### Getting Started

Before writing any code, revisit the existing code if necessary:

- **Explore the models** - Check `app/models/dispatch_request.py`. You may find that approval-related fields already exist from the original design!
- **Review existing patterns** - Look at how other blueprints handle RBAC, routes, and templates
- **Use the MCP tools** - Azure DevOps MCP can help you create and track work items as you go

### Key Areas to Address

| Area | What to Consider |
|------|------------------|
| **Database** | Does `DispatchRequest` need new fields? Status tracking? Audit trail columns? |
| **API Endpoints** | Create, list, approve, reject, cancel. Think about which permissions each requires |
| **UI** | Request form, pending approvals dashboard, user's request history |
| **Security** | RBAC enforcement, preventing self-approval, input validation |
| **Testing** | Unit tests for model logic, API tests, E2E workflow tests |
| **Documentation** | User guide, API docs, README updates |

### Tips for Working with Copilot

- **Be specific** - Tell Copilot exactly what you want: endpoints, fields, permissions
- **Iterate** - Start with the model, then routes, then UI; build incrementally
- **Ask for reviews** - Have Copilot review your code for security issues
- **Provide context** - Reference specific files or areas of the project when prompting Copilot

### Potential API Structure

Consider endpoints like:
- `POST /api/approvals/requests` - Create pending request
- `GET /api/approvals/pending` - Admin view of pending requests
- `GET /api/approvals/my-requests` - User's own requests
- `POST /api/approvals/<id>/approve` - Approve (admin only)
- `POST /api/approvals/<id>/reject` - Reject with reason (admin only)
- `DELETE /api/approvals/<id>` - Cancel own pending request

### Don't Forget

- **Database migrations** - Run `flask db migrate` and `flask db upgrade` after model changes
- **RBAC checks** - Use the existing `@permission_required` decorator pattern
- **Workflow dispatch** - When approved, trigger the actual workflow via the GitHub provider
- **Test coverage** - Aim for 80% coverage on new code
- **Security testing** - Explicitly test that unauthorized actions are blocked

### Bonus Challenges 🎉!

> Do not attempt the bonus challenges until you have fully completed the core requirements above.

If you complete the core requirements early and wish to push your skills further, consider tackling these bonus challenges:

- Add the ability to export all audit events to CSV, excel, or JSON
- Implement email notifications for approvals/rejections using a mock email service
- Create a dashboard view with statistics on approval times, rejection rates, etc.

If you want to push it even farther, consider implementing all of these features in tandem! Remember, you can use Copilot Coding Agent or local background Agent sessions to implement multiple features simultaneously.

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
